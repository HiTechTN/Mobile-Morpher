package com.morpher.mobile.api

import com.morpher.mobile.data.ProcessResponse
import com.morpher.mobile.data.RefactorConfig
import com.morpher.mobile.data.UploadResponse
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

interface MorpherApi {
    @Multipart
    @POST("api/upload")
    suspend fun uploadApk(@Part file: MultipartBody.Part): Response<UploadResponse>

    @POST("api/process/{sessionId}")
    suspend fun processApk(
        @Path("sessionId") sessionId: String,
        @Body config: RefactorConfig,
    ): Response<ProcessResponse>

    @GET("api/download/{sessionId}")
    @Streaming
    suspend fun downloadApk(@Path("sessionId") sessionId: String): Response<okhttp3.ResponseBody>
}

object ApiService {
    private const val DEFAULT_BASE_URL = "http://10.0.2.2:9000/"
    private var customBaseUrl: String? = null

    private val client: OkHttpClient by lazy {
        val builder = OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(120, TimeUnit.SECONDS)
            .writeTimeout(120, TimeUnit.SECONDS)

        if (android.util.Log.isLoggable("MorpherApi", android.util.Log.DEBUG)) {
            val logging = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }
            builder.addInterceptor(logging)
        }

        builder.build()
    }

    fun setBaseUrl(url: String) {
        customBaseUrl = url.trimEnd('/') + "/"
    }

    fun getBaseUrl(): String = customBaseUrl ?: DEFAULT_BASE_URL

    val instance: MorpherApi by lazy {
        Retrofit.Builder()
            .baseUrl(getBaseUrl())
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(MorpherApi::class.java)
    }
}
