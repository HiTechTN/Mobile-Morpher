package com.morpher.mobile.data

import com.google.gson.annotations.SerializedName

data class UploadResponse(
    @SerializedName("session_id")
    val sessionId: String,
    val status: String
)

data class ProcessResponse(
    val status: String,
    @SerializedName("session_id")
    val sessionId: String,
    @SerializedName("refactor_details")
    val refactorDetails: RefactorDetails?,
    val suggestions: List<String>?
)

data class RefactorDetails(
    @SerializedName("manifest_updated")
    val manifestUpdated: Int,
    @SerializedName("smali_updated")
    val smaliUpdated: Int,
    @SerializedName("resources_updated")
    val resourcesUpdated: Int,
    @SerializedName("directories_renamed")
    val directoriesRenamed: Int,
    val errors: List<String>
)

data class RefactorConfig(
    @SerializedName("new_app_name")
    val newAppName: String,
    @SerializedName("new_package_id")
    val newPackageId: String,
    val mode: String = "express",
    @SerializedName("ai_suggestions")
    val aiSuggestions: List<String>? = null
)