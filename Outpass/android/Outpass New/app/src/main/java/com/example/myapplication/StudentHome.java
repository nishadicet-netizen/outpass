package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class StudentHome extends AppCompatActivity {
    Button b1, b2, btstudents, btrequest,btstudentrequest,btrequestoutpass,btviewoutpass,btmessage;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_home);


        b1 = (Button) findViewById(R.id.btlogout);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), Login.class));
            }
        });



        btstudents = (Button) findViewById(R.id.btprofile);

        btstudents.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), StudentProfile.class));
            }
        });




        btrequest = (Button) findViewById(R.id.btrequest);

        btrequest.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), StudentRequestLeave.class));
            }
        });



        btrequestoutpass = (Button) findViewById(R.id.btrequestoutpass);

        btrequestoutpass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), StudentRequestOutpass.class));
            }
        });


        Button b77 = findViewById(R.id.room);
        Button b78 = findViewById(R.id.mess);


        b77.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), ViewRoomAmount.class));
            }
        });


        b78.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), ViewMessAmount.class));
            }
        });

    }
}