import 'package:flutter/material.dart';

class HexColor {
  HexColor(String string);

  static Color fromHex(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length <= 7) buffer.write('ff');
    buffer.write(hexString.replaceFirst('#', ''));

    return Color(int.parse(buffer.toString(), radix: 16));
  }
}
