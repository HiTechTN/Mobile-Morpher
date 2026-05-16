package com.morpher.mobile

import android.app.ProgressDialog
import android.content.ContentValues
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.morpher.mobile.api.ApiService
import com.morpher.mobile.data.RefactorConfig
import kotlinx.coroutines.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity() {

    private lateinit var serverUrlEdit: EditText
    private lateinit var modeSpinner: Spinner
    private lateinit var fileButton: Button
    private lateinit var appNameEdit: EditText
    private lateinit var packageIdEdit: EditText
    private lateinit var transformButton: Button
    private lateinit var statusText: TextView
    private lateinit var progressBar: ProgressBar

    private var selectedFile: File? = null
    private var sessionId: String? = null
    private val scope = CoroutineScope(Dispatchers.Main)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()
        setupListeners()
    }

    private fun initViews() {
        serverUrlEdit = findViewById(R.id.serverUrlEdit)
        modeSpinner = findViewById(R.id.modeSpinner)
        fileButton = findViewById(R.id.fileButton)
        appNameEdit = findViewById(R.id.appNameEdit)
        packageIdEdit = findViewById(R.id.packageIdEdit)
        transformButton = findViewById(R.id.transformButton)
        statusText = findViewById(R.id.statusText)
        progressBar = findViewById(R.id.progressBar)

        val modes = arrayOf("express", "design", "developer")
        modeSpinner.adapter = ArrayAdapter(this, android.R.layout.simple_spinner_dropdown_item, modes)

        serverUrlEdit.setText(ApiService.getBaseUrl())
    }

    private fun setupListeners() {
        serverUrlEdit.setOnFocusChangeListener { _, hasFocus ->
            if (!hasFocus) {
                val url = serverUrlEdit.text.toString().trim()
                if (url.isNotEmpty()) ApiService.setBaseUrl(url)
            }
        }

        fileButton.setOnClickListener {
            val intent = Intent(Intent.ACTION_GET_CONTENT).apply {
                type = "*/*"
            }
            startActivityForResult(Intent.createChooser(intent, "Sélectionner APK"), 1)
        }

        transformButton.setOnClickListener {
            val url = serverUrlEdit.text.toString().trim()
            if (url.isNotEmpty()) ApiService.setBaseUrl(url)
            transformApk()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 1 && resultCode == RESULT_OK) {
            data?.data?.let { uri ->
                selectedFile = File(cacheDir, "temp.apk")
                contentResolver.openInputStream(uri)?.use { input ->
                    selectedFile?.outputStream()?.use { output ->
                        input.copyTo(output)
                    }
                }
                fileButton.text = "Fichier sélectionné"
            }
        }
    }

    private fun transformApk() {
        val appName = appNameEdit.text.toString()
        val packageId = packageIdEdit.text.toString()
        val mode = modeSpinner.selectedItem.toString()

        if (selectedFile == null || appName.isEmpty() || packageId.isEmpty()) {
            showError("Veuillez remplir tous les champs")
            return
        }

        statusText.text = "Upload en cours..."
        progressBar.visibility = android.view.View.VISIBLE
        progressBar.progress = 10
        transformButton.isEnabled = false

        scope.launch {
            try {
                val uploadResponse = ApiService.instance.uploadApk(
                    MultipartBody.Part.createFormData(
                        "file",
                        selectedFile!!.name,
                        selectedFile!!.asRequestBody("application/octet-stream".toMediaTypeOrNull()),
                    ),
                )

                if (!uploadResponse.isSuccessful) {
                    showError("Erreur upload: ${uploadResponse.code()} ${uploadResponse.message()}")
                    return@launch
                }

                progressBar.progress = 40
                sessionId = uploadResponse.body()?.sessionId ?: ""
                statusText.text = "Traitement..."

                val processResponse = ApiService.instance.processApk(
                    sessionId!!,
                    RefactorConfig(appName, packageId, mode),
                )

                if (!processResponse.isSuccessful) {
                    showError("Erreur traitement: ${processResponse.code()} ${processResponse.message()}")
                    return@launch
                }

                progressBar.progress = 70
                statusText.text = "Téléchargement..."

                val downloadResponse = ApiService.instance.downloadApk(sessionId!!)
                if (!downloadResponse.isSuccessful) {
                    showError("Erreur téléchargement: ${downloadResponse.code()}")
                    return@launch
                }

                progressBar.progress = 90
                saveApk(downloadResponse.body()!!.bytes())

            } catch (e: Exception) {
                showError("Erreur: ${e.message ?: e.javaClass.simpleName}")
            } finally {
                progressBar.visibility = android.view.View.GONE
                transformButton.isEnabled = true
            }
        }
    }

    private fun saveApk(data: ByteArray) {
        val fileName = "MobileMorpher-modified.apk"

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val values = ContentValues().apply {
                put(MediaStore.Downloads.DISPLAY_NAME, fileName)
                put(MediaStore.Downloads.MIME_TYPE, "application/vnd.android.package-archive")
                put(MediaStore.Downloads.IS_PENDING, 1)
            }
            val uri = contentResolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
            uri?.let {
                contentResolver.openOutputStream(it)?.use { output ->
                    output.write(data)
                }
                values.clear()
                values.put(MediaStore.Downloads.IS_PENDING, 0)
                contentResolver.update(it, values, null, null)
                statusText.text = "APK sauvegardé dans Téléchargements"
            }
        } else {
            val downloadsDir = Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DOWNLOADS,
            )
            val file = File(downloadsDir, fileName)
            FileOutputStream(file).use { it.write(data) }
            statusText.text = "APK sauvegardé dans Téléchargements"
        }

        progressBar.progress = 100
        AlertDialog.Builder(this)
            .setTitle("Succès")
            .setMessage("APK transformé et sauvegardé dans Téléchargements/$fileName")
            .setPositiveButton("OK", null)
            .show()
    }

    private fun showError(msg: String) {
        statusText.text = "Erreur: $msg"
        AlertDialog.Builder(this)
            .setTitle("Erreur")
            .setMessage(msg)
            .setPositiveButton("OK", null)
            .show()
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
