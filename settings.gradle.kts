pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
    plugins {
        // Provide plugin versions for the plugins used in build scripts
        id("com.android.application") version "8.1.0"
        id("org.jetbrains.kotlin.android") version "1.9.10"
    }
}

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "kutup_navigasyon"
