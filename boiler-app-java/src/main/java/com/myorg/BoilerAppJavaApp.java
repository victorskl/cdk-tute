package com.myorg;

import software.amazon.awscdk.core.App;

import java.util.Arrays;

public class BoilerAppJavaApp {
    public static void main(final String[] args) {
        App app = new App();

        new BoilerAppJavaStack(app, "BoilerAppJavaStack");

        app.synth();
    }
}
