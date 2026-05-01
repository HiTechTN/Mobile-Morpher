package com.morpher.mobile.api

import com.morpher.mobile.data.ProcessResponse
import com.morpher.mobile.data.RefactorConfig
import com.morpher.mobile.data.UploadResponse
import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.*

interface MorpherApi {
    @Multipart
    @POST("api/upload")
    suspend fun uploadApk(@Part file: MultipartBody.Part): Response<UploadResponse>
    
    @POST("api/process/{sessionId}")
    suspend fun processApk(
        @Path("sessionId") sessionId: String,
        @Body config: RefactorConfig
    ): Response<ProcessResponse>
    
    @GET("api/download/{sessionId}")
    suspend fun downloadApk(@Path("sessionId") sessionId: String)
}

object ApiService {
    private const val BASE_URL = "http://10.0.2.2:9000/" // Android emulator localhost
    
    val instance: MorpherApi by lazy {
        retrofit2.Retrofit.Builder()
            .baseUrl(BASE_URL)
            .build()
            .create(MorpherApi::class.java)
    }
}