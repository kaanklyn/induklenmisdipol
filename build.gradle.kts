plugins {
    id("com.android.application")
    kotlin("android")
}

android {
    namespace = "com.kutup.navigasyon"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.kutup.navigasyon"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")

    implementation("androidx.camera:camera-core:1.3.0-beta01")
    implementation("androidx.camera:camera-camera2:1.3.0-beta01")
    implementation("androidx.camera:camera-lifecycle:1.3.0-beta01")
    implementation("androidx.camera:camera-view:1.3.0-beta01")


    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1")

    implementation("com.google.android.material:material:1.10.0")

    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.2")

    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}
