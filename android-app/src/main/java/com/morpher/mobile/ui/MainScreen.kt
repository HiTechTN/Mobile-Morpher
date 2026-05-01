package com.morpher.mobile.ui

import android.content.Context
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.morpher.mobile.api.ApiService
import com.morpher.mobile.data.RefactorConfig
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import java.io.File

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen() {
    val context = LocalContext.current
    var selectedMode by remember { mutableStateOf("express") }
    var appName by remember { mutableStateOf("") }
    var packageId by remember { mutableStateOf("") }
    var status by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    var progress by remember { mutableFloatStateOf(0f) }
    var resultUrl by remember { mutableStateOf("") }
    var selectedFileUri by remember { mutableStateOf<Uri?>(null) }
    
    val scope = rememberCoroutineScope()
    
    val filePicker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        selectedFileUri = uri
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Header
        Text(
            text = "🧬 Mobile-Morpher",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.primary
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = "Transformez vos APK Android",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Mode Selection
        Text(
            text = "Mode de transformation",
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.fillMaxWidth()
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            listOf("express" to "⚡ Express", "design" to "🎨 Design", "developer" to "🔧 Dev").forEach { (mode, label) ->
                FilterChip(
                    selected = selectedMode == mode,
                    onClick = { selectedMode = mode },
                    label = { Text(label) },
                    modifier = Modifier.weight(1f)
                )
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // File Selection
        OutlinedButton(
            onClick = { filePicker.launch("*/*") },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if (selectedFileUri != null) "✅ Fichier sélectionné" else "📁 Sélectionner un APK")
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // App Name
        OutlinedTextField(
            value = appName,
            onValueChange = { appName = it },
            label = { Text("Nom de l'application") },
            placeholder = { Text("Mon Application") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        // Package ID
        OutlinedTextField(
            value = packageId,
            onValueChange = { packageId = it },
            label = { Text("Package ID") },
            placeholder = { Text("com.monapp.pro") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Progress
        if (isLoading) {
            LinearProgressIndicator(
                progress = { progress },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))
        }
        
        // Status
        if (status.isNotEmpty()) {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(
                    containerColor = if (status.contains("succès") || status.contains("télécharger"))
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.2f)
                    else MaterialTheme.colorScheme.error.copy(alpha = 0.2f)
                )
            ) {
                Text(
                    text = status,
                    modifier = Modifier.padding(12.dp),
                    color = if (status.contains("succès") || status.contains("télécharger"))
                        MaterialTheme.colorScheme.tertiary
                    else MaterialTheme.colorScheme.error
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
        }
        
        // Submit Button
        Button(
            onClick = {
                if (selectedFileUri == null || appName.isEmpty() || packageId.isEmpty()) {
                    status = "Veuillez remplir tous les champs"
                    return@Button
                }
                
                scope.launch {
                    try {
                        isLoading = true
                        status = "Upload en cours..."
                        progress = 0.2f
                        
                        // Get file from URI
                        val inputStream = selectedFileUri?.let {
                            context.contentResolver.openInputStream(it)
                        }
                        if (inputStream == null) {
                            status = "Erreur: Impossible de lire le fichier"
                            isLoading = false
                            return@launch
                        }
                        
                        // Create temp file
                        val tempFile = File.createTempFile("upload", ".apk", context.cacheDir)
                        tempFile.outputStream().use { output ->
                            inputStream.copyTo(output)
                        }
                        
                        // Upload
                        val uploadResponse = ApiService.instance.uploadApk(
                            MultipartBody.Part.createFormData(
                                "file",
                                tempFile.name,
                                tempFile.asRequestBody("application/vnd.android.package-archive".toMediaTypeOrNull())
                            )
                        )
                        
                        if (!uploadResponse.isSuccessful) {
                            status = "Erreur upload: ${uploadResponse.code()}"
                            isLoading = false
                            return@launch
                        }
                        
                        val sessionId = uploadResponse.body()?.sessionId ?: ""
                        progress = 0.4f
                        status = "Traitement en cours..."
                        
                        // Process
                        val processResponse = ApiService.instance.processApk(
                            sessionId,
                            RefactorConfig(appName, packageId, selectedMode)
                        )
                        
                        if (!processResponse.isSuccessful) {
                            status = "Erreur traitement: ${processResponse.code()}"
                            isLoading = false
                            return@launch
                        }
                        
                        progress = 0.8f
                        status = "✅ Transformation réussie!"
                        resultUrl = "http://localhost:9000/api/download/$sessionId"
                        progress = 1f
                        
                    } catch (e: Exception) {
                        status = "❌ Erreur: ${e.message}"
                    } finally {
                        isLoading = false
                    }
                }
            },
            enabled = !isLoading,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if (isLoading) "Traitement..." else "Transformer l'APK")
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Info
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surface
            )
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                Text(
                    text = "Configuration API",
                    style = MaterialTheme.typography.titleSmall
                )
                Text(
                    text = "Par défaut: http://10.0.2.2:9000 (émulateur)",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                )
            }
        }
    }
}