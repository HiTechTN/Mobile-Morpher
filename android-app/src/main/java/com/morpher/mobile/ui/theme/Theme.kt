package com.morpher.mobile.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF6366f1),
    secondary = Color(0xFFec4899),
    tertiary = Color(0xFF22c55e),
    background = Color(0xFF0f172a),
    surface = Color(0xFF1e293b)
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF6366f1),
    secondary = Color(0xFFec4899),
    tertiary = Color(0xFF22c55e),
    background = Color(0xFFf8fafc),
    surface = Color(0xFFffffff)
)

@Composable
fun MorpherTheme(
    darkTheme: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = DarkColorScheme
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}