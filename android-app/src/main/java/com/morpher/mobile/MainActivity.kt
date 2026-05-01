package com.morpher.mobile

import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.morpher.mobile.api.ApiService
import com.morpher.mobile.data.RefactorConfig
import kotlinx.coroutines.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody

class MainActivity : AppCompatActivity() {
    
    private lateinit var modeSpinner: Spinner
    private lateinit var fileButton: Button
    private lateinit var appNameEdit: EditText
    private lateinit var packageIdEdit: EditText
    private lateinit var transformButton: Button
    private lateinit var statusText: TextView
    private lateinit var progressBar: ProgressBar
    
    private var selectedFile: java.io.File? = null
    private val scope = CoroutineScope(Dispatchers.Main)
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        setupListeners()
    }
    
    private fun initViews() {
        modeSpinner = findViewById(R.id.modeSpinner)
        fileButton = findViewById(R.id.fileButton)
        appNameEdit = findViewById(R.id.appNameEdit)
        packageIdEdit = findViewById(R.id.packageIdEdit)
        transformButton = findViewById(R.id.transformButton)
        statusText = findViewById(R.id.statusText)
        progressBar = findViewById(R.id.progressBar)
        
        val modes = arrayOf("express", "design", "developer")
        modeSpinner.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, modes)
    }
    
    private fun setupListeners() {
        fileButton.setOnClickListener {
            val intent = android.content.Intent(android.content.Intent.ACTION_GET_CONTENT).apply {
                type = "*/*"
            }
            startActivityForResult(android.content.Intent.createChooser(intent, "Sélectionner APK"), 1)
        }
        
        transformButton.setOnClickListener {
            transformApk()
        }
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: android.content.Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 1 && resultCode == RESULT_OK) {
            data?.data?.let { uri ->
                selectedFile = java.io.File(cacheDir, "temp.apk")
                contentResolver.openInputStream(uri)?.use { input ->
                    selectedFile?.outputStream()?.use { output ->
                        input.copyTo(output)
                    }
                }
                fileButton.text = "✅ Fichier sélectionné"
            }
        }
    }
    
    private fun transformApk() {
        val appName = appNameEdit.text.toString()
        val packageId = packageIdEdit.text.toString()
        val mode = modeSpinner.selectedItem.toString()
        
        if (selectedFile == null || appName.isEmpty() || packageId.isEmpty()) {
            statusText.text = "Veuillez remplir tous les champs"
            return
        }
        
        statusText.text = "Upload en cours..."
        progressBar.visibility = View.VISIBLE
        transformButton.isEnabled = false
        
        scope.launch {
            try {
                val uploadResponse = ApiService.instance.uploadApk(
                    MultipartBody.Part.createFormData(
                        "file",
                        selectedFile!!.name,
                        selectedFile!!.asRequestBody("application/octet-stream".toMediaTypeOrNull())
                    )
                )
                
                if (!uploadResponse.isSuccessful) {
                    statusText.text = "Erreur upload"
                    return@launch
                }
                
                val sessionId = uploadResponse.body()?.sessionId ?: ""
                statusText.text = "Traitement..."
                
                val processResponse = ApiService.instance.processApk(
                    sessionId,
                    RefactorConfig(appName, packageId, mode)
                )
                
                if (processResponse.isSuccessful) {
                    statusText.text = "✅ Succès! APK transformé"
                } else {
                    statusText.text = "Erreur traitement"
                }
            } catch (e: Exception) {
                statusText.text = "Erreur: ${e.message}"
            } finally {
                progressBar.visibility = View.GONE
                transformButton.isEnabled = true
            }
        }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}