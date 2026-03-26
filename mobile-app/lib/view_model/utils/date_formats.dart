
//Date Format yyyy-mm-dd
String formatDate(String inputDate) {
  DateTime dateTime = DateTime.parse(inputDate);
  String formattedDate =
      "${dateTime.year}-${dateTime.month.toString().padLeft(2, '0')}-${dateTime.day.toString().padLeft(2, '0')}";
  return formattedDate;
}
