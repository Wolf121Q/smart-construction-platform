import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';

void funToast(String ToastMessage, Color custcolor) {
  Fluttertoast.showToast(
      msg: ToastMessage,
      toastLength: Toast.LENGTH_LONG,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: custcolor,
      textColor: Colors.white,
      fontSize: 16.0);
}
