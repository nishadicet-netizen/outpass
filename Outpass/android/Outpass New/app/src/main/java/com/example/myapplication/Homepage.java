package com.example.myapplication;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class Homepage extends AppCompatActivity {

    Button b1, b2, btstudents, btrequest,btstudentrequest,btrequestoutpass,btviewoutpass,btmessage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_homepage);

        b1 = (Button) findViewById(R.id.btlogout);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), Login.class));
            }
        });



        btstudents = (Button) findViewById(R.id.btstudents);

        btstudents.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


//                startActivity(new Intent(getApplicationContext(), TeacherManageStudents.class));
            }
        });

        btrequest = (Button) findViewById(R.id.btrequest);

        btrequest.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), TeacherRequestLeave.class));
            }
        });
        btstudentrequest = (Button) findViewById(R.id.btstudentrequest);

        btstudentrequest.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), TeacherViewLeaveRequestFromStudent.class));
            }
        });

        btrequestoutpass = (Button) findViewById(R.id.btrequestoutpass);

        btrequestoutpass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), TeacherRequestOutpass.class));
            }
        });

        btviewoutpass = (Button) findViewById(R.id.btviewoutpass);

        btviewoutpass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                startActivity(new Intent(getApplicationContext(), TeacherViewOutpass.class));
            }
        });







    }
}