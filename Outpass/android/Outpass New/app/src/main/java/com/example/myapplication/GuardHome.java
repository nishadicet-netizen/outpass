package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class GuardHome extends AppCompatActivity {
    Button b1, b2, btstudents, btscan,btstudentrequest,btrequestoutpass,btviewoutpass,btlate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_guard_home);



        b1 = (Button) findViewById(R.id.btlogout);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), Login.class));
            }
        });



        btscan = (Button) findViewById(R.id.btscan);

        btscan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), AndroidBarcodeQrExample.class));
            }
        });


        btlate = (Button) findViewById(R.id.btlate);

        btlate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), GuardSendLateComing.class));
            }
        });
    }
}