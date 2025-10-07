package com.example.myapplication;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.ImageView;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import com.squareup.picasso.Picasso;

public class TeacherViewSanctionedQrForOutPass extends AppCompatActivity {
    ListView lv1;
    String image;

    ImageView im;
    SharedPreferences sh;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teacher_view_sanctioned_qr_for_out_pass);
        sh= PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        im=(ImageView) findViewById(R.id.imageView);
        image=StudentRequestOutpass.qrs;

        String pth = "http://"+sh.getString("ip", "")+"/"+image;
        pth = pth.replace("~", "");
//	       Toast.makeText(context, pth, Toast.LENGTH_LONG).show();

        Log.d("-------------", pth);



        Picasso.with(getApplicationContext())
                .load(pth)
                .placeholder(R.drawable.ic_launcher_background)
                .error(R.drawable.ic_launcher_background).into(im);





    }
}
