import 'dart:io' show File, Platform, SocketException;

import 'dart:math';

import 'package:connectivity/connectivity.dart';
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/animation/animated_checkmark_dialog.dart';
import 'package:dha_ctt_app/model/resources/string_manager.dart';
import 'package:dha_ctt_app/model/shared_preferences/share_pref_api_function.dart';
import 'package:dha_ctt_app/view/screens/dashboard/home.dart';
import 'package:dha_ctt_app/view/screens/pending_task/pending_task.dart';

import 'package:dha_ctt_app/view/widgets/app_bar/custom_app_bar.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/card_Image_widget.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_dialog.dart';
import 'package:dha_ctt_app/view/widgets/dialogs/custom_toast.dart';

import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/category_model.dart';
import 'package:dha_ctt_app/view_model/view_models/new_complaint_model/complaint_status_model.dart';
import 'package:dio/dio.dart';

import 'package:dropdown_textfield/dropdown_textfield.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:overlay_loader_with_app_icon/overlay_loader_with_app_icon.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:geolocator/geolocator.dart';


class NewComplaint extends StatefulWidget {
  final int areaId;
  NewComplaint({
    required this.areaId,
  });

  @override
  State<NewComplaint> createState() => _NewComplaintState();
}

class _NewComplaintState extends State<NewComplaint> {
  String appBaseUrl = AppStrings.appBaseUrl;
  String appNewcomplaint = AppStrings.NEW_COMPLAINT;
  String appGetCategory = AppStrings.GET_CATEGORY;
  String appComplaintStatuses = AppStrings.COMPLAINT_STATUS;
  SingleValueDropDownController? _cnt;
  SingleValueDropDownController? _Subcnt;
  final _formKey = GlobalKey<FormState>();

  Future<bool> isInternetConnected() async {
    var connectivityResult = await (Connectivity().checkConnectivity());
    return connectivityResult != ConnectivityResult.none;
  }

  dynamic _category;
  dynamic _catID;
  dynamic _subcategory;
  dynamic _subCatID;
  dynamic _status;
  dynamic _statusId;

  late int _areaId = widget.areaId;
  String _description = '';
  String? latitude;
  String? longitude;

  int _progress = 0;
  dynamic path = '';
  String? currentTime;
  List<DropDownValueModel> dropDownList = [];
  List<DropDownValueModel> subcategoryList = [];
  List<DropDownValueModel> complaintStatus = [];
  List<Item> chatagoriDataArray = [];
  List<ComplaintStatusesModel> complaintStatusesModel = [];
  int selectedCategory = 0;
  String filePath = "";

  bool _isLoading = false;

// Function to retrieve categories from SharedPreferences and populate the list
  Future<void> getCategoriesFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? serializedData = prefs.getString('chatagoriDataArray');

      if (serializedData != null && serializedData.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(serializedData);

        chatagoriDataArray =
            dataArray.map((json) => Item.fromJson(json)).toList();

        // Update the dropdown lists if needed
        final updatedDropDownList = <DropDownValueModel>[];
        chatagoriDataArray.forEach((item) {
          // Use the category id as the value and the name as the name
          // Check if the category id is 0 before adding to the list

          if (item.parent == 0) {
            updatedDropDownList.add(DropDownValueModel(
              name: item.name,
              value: item.id,
            ));
          }
          // print("Step 2: ${updatedDropDownList}");
        });

        setState(() {
          dropDownList =
              updatedDropDownList; // Update the category dropdown list

          subcategoryList.clear();
          subcategoryList = [];
          //     selectedCategory); // Update the subcategory dropdown list
        });
      } else {
        print('No category data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving category data from SharedPreferences: $e');
    }
  }

// Function to retrieve status from SharedPreferences and populate the list
  Future<void> getStatusFromSharedPreferences() async {
    try {
      final SharedPreferences prefs = await SharedPreferences.getInstance();
      final String? statusDataSerialzed = prefs.getString('statusDataArray');

      if (statusDataSerialzed != null && statusDataSerialzed.isNotEmpty) {
        final List<dynamic> dataArray = jsonDecode(statusDataSerialzed);

        complaintStatusesModel = dataArray
            .map((json) => ComplaintStatusesModel.fromJson(json))
            .toList();

        // Update the dropdown lists if needed
        final updatedStatusList = <DropDownValueModel>[];
        complaintStatusesModel.forEach((status) {
          // Use the category id as the value and the name as the name
          // Check if the category id is 0 before adding to the list

          updatedStatusList.add(DropDownValueModel(
            name: status.name,
            value: status.id,
          ));
        });

        // print("Step 5: ${updatedStatusList}");

        setState(() {
          complaintStatus = updatedStatusList; // Update the status list
        });
      } else {
        print('No Status data found in SharedPreferences.');
      }
    } catch (e) {
      print('Error retrieving category data from SharedPreferences: $e');
    }
  }

  // getting Category ID
  Future<int?> getCategoryIdByName(String categoryName) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String storedData = prefs.getString('chatagoriDataArray') ?? '';

    if (storedData.isNotEmpty) {
      final List<dynamic> dataArray = jsonDecode(storedData);

      print("Catewgory: " + dataArray.toString());

      for (var jsonData in dataArray) {
        final Item chatagoriData = Item.fromJson(jsonData);

        if (chatagoriData.name == categoryName) {
          selectedCategory = chatagoriData.id;
          print(chatagoriData.id);
          return chatagoriData.id;
        }
      }
    } else {
      print("storedData is Empty!");
    }

    return null; // Return null if category name is not found
  }

// Function to get subcategories by category ID
  List<DropDownValueModel> getSubcategoriesByCategoryId(
      List<Item> chatagoriDataArray, int categoryId) {
    List<DropDownValueModel> subcategories = [];

    for (var item in chatagoriDataArray) {
      if (item.parent == categoryId) {
        // Only add items with a category ID matching the selected category,
        // and exclude items with the same ID as the category (main category).
        subcategories.add(DropDownValueModel(
          name: item.name,
          value: item.id,
        ));
      }
    }
    print("Step 3: ${subcategories}");

    return subcategories;
  }

  Future<int?> getCategoryIdFromName(String categoryName) async {
    final prefs = await SharedPreferences.getInstance();
    final storedData = prefs.getString('chatagoriDataArray');

    if (storedData != null) {
      final List<dynamic> dataArray = jsonDecode(storedData);

      for (var jsonData in dataArray) {
        final Item chatagoriData = Item.fromJson(jsonData);

        if (chatagoriData.name == categoryName) {
          return chatagoriData.id;
        }
      }
    }
    //("this is comming from shared pref: " + chatagoriData.id.toString());
    return null; // Return null if category name is not found
  }

  //Get Complaint submittime id for uploading file.
  int extractIdFromApiResponse(String responseBody) {
    Map<String, dynamic> responseJson = json.decode(responseBody);
    print(responseJson);

    if (responseJson.containsKey("data")) {
      Map<String, dynamic> dataArray = responseJson["data"];
      if (dataArray.containsKey("id")) {
        int id = dataArray["id"];
        return id;
      }
    }

    // Return a default value or handle the case when id is not found
    return -1; // You can choose a suitable default value or error indicator
  }

  // Future<void> enqueueComplaint(Map<String, dynamic> complaint) async {
  //   final prefs = await SharedPreferences.getInstance();
  //   await prefs.setString('queued_complaints', jsonEncode(complaint));
  // }

//Store local complaints
  Future<void> enqueueComplaint(Map<String, dynamic> complaint) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final List<String> queuedComplaints =
          prefs.getStringList('queued_complaints') ?? [];
      queuedComplaints.add(jsonEncode(complaint));
      await prefs.setStringList('queued_complaints', queuedComplaints);
      Navigator.of(context)
          .push(MaterialPageRoute(builder: (context) => PendingTask()));
    } catch (e) {
      print('Error: $e');
      // Handle the error appropriately
    }
  }

//Post Compalint
  Future<void> postComplaintData() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String token = prefs.getString('access_token') ?? '';

    if (token.isEmpty) {
      print('Access token is empty');
      return;
    }
    print(token);

    Map<String, String> headers = {
      'Authorization': 'Bearer $token',
    };

    // Create a Random instance to generate a boundary
    var random = Random();
    var boundary = '---------------------------${random.nextInt(1000000000)}';

    // Set Content-Type with boundary parameter
    headers['Content-Type'] = 'multipart/form-data; boundary=$boundary';

    // Create a FormData object to send as the request body
    var formData = FormData.fromMap({
      'status_id': _statusId.toString(),
      'category_id': _catID.toString(),
      'subcategory_id': _subCatID.toString(),
      'area_id': _areaId.toString(),
      'description': _description.toString(),
      'latitude': latitude.toString(),
      'longitude': longitude.toString(),
      'attachments': await MultipartFile.fromFile(filePath),
    });

    printSelectedValues();

    // Send the request using Dio (an HTTP client for Dart)
    var dio = Dio();
    var response = await dio.post(
      appBaseUrl + appNewcomplaint,
      data: formData,
      options: Options(
        headers: headers,
      ),
    );

    print("Responce Data: ${response.data}");

    if (response.statusCode == 200 || response.statusCode == 201) {
      print("Data Upload Successfully....");
      // final responseData = response.data;
      // Map<String, dynamic> responseJson = json.decode(responseData);

      // print("Responce Json: ${responseJson.toString()}");

      showAnimatedCheckmarkDialog(context, 'Complaint Registered!', appcolor);

      _isLoading = false;
      storeTracComlaintkList();
      storeDashboardChartApi();
      await Future.delayed(Duration(seconds: 1));

      final route = MaterialPageRoute(builder: (context) => Home());
      Navigator.pushAndRemoveUntil(context, route, (route) => false);
    } else {
      _isLoading = false;
      // Error handling

      print('API Error: ${response.statusCode}+${response.data}');

      // Show a simple dialog with the API error message
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: Text('Server Side Issue!'),
            children: <Widget>[
              SimpleDialogOption(
                onPressed: () {
                  Navigator.of(context).pop(); // Close the dialog
                },
                child: Text(
                    'Something Went Wrong! ' + response.statusCode.toString()),
              ),
            ],
          );
        },
      );
    }
  }

  // Dialog fuction
  void showCustomDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(
            "Select Action!",
            textAlign: TextAlign.center,
          ),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: appcolor,
                  ),
                  onPressed: () async {
                    String fPath = "";
                    String? imagePath = await useImageFromCamera();
                    setState(() {});
                    print("File Name: " + imagePath.toString());
                    if (imagePath != null) {
                      filePath = imagePath.toString();
                      Navigator.of(context).pop(); // Close the dialog
                    }

                    File imageFile = File(filePath);

                    try {
                      int fileSize4MB = (4 * 1024); //4MB

                      int fileSizeMB = imageFile.lengthSync(); // file length

                      if (fileSizeMB <= fileSize4MB) {
                        filePath = filePath;

                        print('File size: $filePath');
                      }
                    } catch (error) {
                      print('Upload error: $error');

                      // Show a simple dialog with the error message
                    }
                  },
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Take a Photo",
                        style: TextStyle(
                          color: dfColor,
                        ),
                      ),
                      Icon(
                        Icons.camera,
                        color: dfColor,
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 20),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: appcolor,
                  ),
                  onPressed: () async {
                    String fPath = "";
                    String? imagePath = await useImageFromGallery();
                    setState(() {});
                    print("File Name: " + imagePath.toString());
                    if (imagePath != null) {
                      filePath = imagePath.toString();
                      Navigator.of(context).pop(); // Close the dialog
                    }

                    File imageFile = File(filePath);

                    try {
                      int fileSize4MB = (4 * 1024); //4MB

                      int fileSizeMB = imageFile.lengthSync(); // file length

                      if (fileSizeMB <= fileSize4MB) {
                        filePath = filePath;

                        print('File size: $filePath');
                      }
                    } catch (error) {
                      print('Upload error: $error');

                      // Show a simple dialog with the error message
                    }
                  },
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Choose From Gallery",
                        style: TextStyle(
                          color: dfColor,
                        ),
                      ),
                      Icon(
                        Icons.photo_library_outlined,
                        color: dfColor,
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 10),
              ],
            ),
          ),
        );
      },
    );
  }

  //Image From Gallery
  Future<String?> useImageFromGallery() async {
    // Add code to open image picker and return the selected image path
    // For example, using the image_picker package
    final pickedImage =
        await ImagePicker().pickImage(source: ImageSource.gallery);
    print("Use gallery: ${pickedImage?.path.toString()}");
    if (pickedImage != null) {
      return pickedImage.path;
    }
    return null; // Return null if no image is selected
  }

  //Image From Gallery
  Future<String?> useImageFromCamera() async {
    // Add code to open image picker and return the selected image path
    // For example, using the image_picker package
    final pickedImage =
        await ImagePicker().pickImage(source: ImageSource.camera);
    print("Use Camera: ${pickedImage?.path.toString()}");
    if (pickedImage != null) {
      return pickedImage.path;
    }
    return null; // Return null if no image is selected
  }

//submitting
  void printSelectedValues() async {
    print("Selected Category: $_catID");
    print("Selected Subcategory: $_subCatID");
    print("Selected Status: $_statusId");
    print("Selected Area: ${widget.areaId}");
    print("Selected Description: $_description");
    // print("Selected Progress: ${_progress}");
    print("Selected latitude: ${latitude}");
    print("Selected longitude: ${longitude}");
  }

  Future<void> getLocation() async {
    Position position;
    try {
      position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        latitude = '${position.latitude}';
        longitude = '${position.longitude}';
      });
    } catch (e) {
      print("Error while getting location: $e");
    }
  }

  @override
  void initState() {
    super.initState();
    getCategoriesFromSharedPreferences();
    getStatusFromSharedPreferences();
    // storeCategorieslistApi();
    storeStatusApi();
    getLocation();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
  }

  bool ckError = false;

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scheight = MediaQuery.of(context).size.height;
    return Scaffold(
      backgroundColor: drakGreyColor,
      appBar: CustomAppBar(
          navFunction: () {
            Navigator.of(context).pop();
          },
          lastIcon: Icons.info_outline,
          infoFunction: () {
            CustomDialog(context);
          }),
      body: OverlayLoaderWithAppIcon(
        overlayBackgroundColor: appcolor,
        isLoading: _isLoading,
        // isLoading: _isLoading,
        appIcon: CircularProgressIndicator(),
        // appIcon: Image.asset(
        //   "asserts/icons/app_icon.png",
        //   width: 40,
        // ),
        child: SingleChildScrollView(
          child: Container(
            height: Platform.isAndroid ? scheight / 1.25 : scheight / 1.35,
            width: scWidth,
            color: drakGreyColor,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  // color: appcolor,
                  width: scWidth,
                  alignment: Alignment.center,
                  margin: EdgeInsets.only(
                    bottom: marginLR,
                  ),
                  padding: EdgeInsets.only(top: scheight / 50, bottom: 0),
                  child: Text(
                    "Register Your Complaint",
                    style: TextStyle(
                      color: appcolor,
                      fontWeight: FontWeight.w600,
                      fontSize: lgFontSize,
                    ),
                  ),
                ),
                Container(
                  margin: EdgeInsets.only(
                      left: marginLR, right: marginLR, top: scheight / 60),
                  child: Form(
                    key: _formKey,
                    child: Stack(
                      children: [
                        SingleChildScrollView(
                          child: Container(
                            margin: EdgeInsets.only(bottom: scheight / 10),
                            padding: EdgeInsets.symmetric(
                                horizontal: marginLR, vertical: scheight / 140),
                            height: ckError == true
                                ? scheight / 1.79
                                : filePath.isEmpty
                                    ? Platform.isAndroid
                                        // ? scheight / 2.05
                                        ? scheight / 2.019
                                        : scheight / 2.2
                                    : Platform.isAndroid
                                        ? scheight / 1.65
                                        : scheight / 1.85,
                            decoration: BoxDecoration(
                                color: dfColor,
                                borderRadius: BorderRadius.circular(15)),
                            child: SingleChildScrollView(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Container(
                                    margin:
                                        EdgeInsets.only(top: scheight / 300),
                                    child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            "Category",
                                            style: TextStyle(
                                                fontSize: exSmFontSize,
                                                fontWeight: FontWeight.w500,
                                                color: appcolor),
                                          ),
                                          DropDownTextField(
                                            // initialValue: "name4",
                                            // readOnly: true,
                                            controller: _cnt,
                                            clearOption: true,
                                            dropDownIconProperty: IconProperty(
                                                icon:
                                                    Icons.keyboard_arrow_down),

                                            keyboardType: TextInputType.number,
                                            autovalidateMode:
                                                AutovalidateMode.disabled,
                                            clearIconProperty: IconProperty(
                                                color: Colors.green),

                                            validator: (value) {
                                              if (value!.isEmpty) {
                                                return "Please Select Category";
                                              }
                                              return null;
                                            },
                                            // dropDownItemCount: 6,

                                            dropDownList: dropDownList,
                                            onChanged: (value) {
                                              _Subcnt =
                                                  SingleValueDropDownController();
                                              setState(() {
                                                _category = value.name;
                                                _catID = value.value;

                                                print(
                                                    "Cat Name: ${_category}, cat id: ${_catID}");
                                              });

                                              getCategoryIdByName(
                                                      _category.toString())
                                                  .then((categoryId) {
                                                if (categoryId != null) {
                                                  _catID = categoryId;
                                                  setState(() {
                                                    selectedCategory =
                                                        categoryId;
                                                    subcategoryList.clear();
                                                    _subcategory = null;
                                                    _Subcnt =
                                                        SingleValueDropDownController();
                                                    subcategoryList =
                                                        getSubcategoriesByCategoryId(
                                                            chatagoriDataArray,
                                                            selectedCategory);
                                                  });
                                                } else {
                                                  // Handle the case when the category is not found
                                                  print("Category not found.");
                                                }
                                              });
                                            },
                                          ),
                                        ]),
                                  ),

                                  //------------------

                                  Container(
                                    margin: EdgeInsets.only(top: scheight / 90),
                                    child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            "Sub Category",
                                            style: TextStyle(
                                                fontSize: exSmFontSize,
                                                fontWeight: FontWeight.w500,
                                                color: appcolor),
                                          ),
                                          DropDownTextField(
                                            // initialValue: "name4",
                                            // readOnly: true,
                                            controller: _Subcnt,
                                            clearOption: true,
                                            dropDownIconProperty: IconProperty(
                                                icon:
                                                    Icons.keyboard_arrow_down),

                                            keyboardType: TextInputType.number,
                                            autovalidateMode:
                                                AutovalidateMode.disabled,
                                            clearIconProperty: IconProperty(
                                                color: Colors.green),

                                            validator: (value) {
                                              if (value!.isEmpty) {
                                                return "Please Select Sub Category";
                                              }
                                              return null;
                                            },
                                            // dropDownItemCount: 6,

                                            dropDownList: subcategoryList,
                                            onChanged: (value) {
                                              setState(() {
                                                _subcategory = value.name;
                                                _subCatID = value.value;

                                                print(
                                                    "SubCat Name: ${_subcategory}, Subcat id: ${_subCatID}");
                                              });
                                            },
                                          ),
                                        ]),
                                  ),

                                  //------------------

                                  Container(
                                    margin: EdgeInsets.only(top: scheight / 90),
                                    child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            "Status",
                                            style: TextStyle(
                                                fontSize: exSmFontSize,
                                                fontWeight: FontWeight.w500,
                                                color: appcolor),
                                          ),
                                          DropDownTextField(
                                            // initialValue: "name4",
                                            // readOnly: true,
                                            controller: _cnt,
                                            clearOption: true,
                                            dropDownIconProperty: IconProperty(
                                                icon:
                                                    Icons.keyboard_arrow_down),

                                            keyboardType: TextInputType.number,
                                            autovalidateMode:
                                                AutovalidateMode.disabled,
                                            clearIconProperty: IconProperty(
                                                color: Colors.green),

                                            validator: (value) {
                                              if (value!.isEmpty) {
                                                return "Please Select Status";
                                              }
                                              return null;
                                            },
                                            // dropDownItemCount: 6,

                                            dropDownList: complaintStatus,
                                            onChanged: (value) {
                                              setState(() {
                                                _status = value.name;
                                                _statusId = value.value;

                                                print(
                                                    "Status Name: ${_status}, status id: ${_statusId}");
                                              });
                                            },
                                          ),
                                        ]),
                                  ),

                                  //------------------

                                  Container(
                                    margin: EdgeInsets.only(top: scheight / 90),
                                    child: TextFormField(
                                      textInputAction: TextInputAction.next,
                                      autofocus: false,
                                      minLines: 1,
                                      maxLength: 500,
                                      maxLines: 5,
                                      style: TextStyle(
                                        fontSize: 19.0,
                                        color: Colors.black87,
                                      ),
                                      decoration: InputDecoration(
                                        hintText:
                                            "Type your complaint (Max 500 Characters)",
                                        hintStyle: TextStyle(
                                            color: Colors.black45,
                                            fontSize: 12),
                                        filled: true,
                                        fillColor: drakGreyColor,
                                        contentPadding: const EdgeInsets.only(
                                            left: 15.0,
                                            bottom: 15.0,
                                            top: 15.0,
                                            right: 15.0),
                                        focusedBorder: OutlineInputBorder(
                                          borderSide:
                                              BorderSide(color: Colors.white),
                                          borderRadius:
                                              BorderRadius.circular(8),
                                        ),
                                        enabledBorder: UnderlineInputBorder(
                                          borderSide:
                                              BorderSide(color: Colors.white),
                                          borderRadius:
                                              BorderRadius.circular(8),
                                        ),
                                      ),
                                      keyboardType: TextInputType.text,
                                      inputFormatters: <TextInputFormatter>[
                                        FilteringTextInputFormatter.allow(
                                            RegExp(r'[a-zA-Z0-9. ]'))
                                      ],
                                      validator: (value) {
                                        if (value!.isEmpty) {
                                          setState(() {
                                            ckError = true;
                                          });
                                          return 'Please write your complaint';
                                        }

                                        // Define a regular expression pattern to match alphabets, numbers, and full stops
                                        final RegExp pattern =
                                            RegExp(r'^[a-zA-Z0-9. ]*$');

                                        if (!pattern.hasMatch(value)) {
                                          return 'Only alphabets, numbers, and full stops are allowed';
                                        }

                                        return null;
                                      },
                                      onChanged: (value) {
                                        ckError = false;
                                        setState(() {
                                          _description = value.trim();

                                          print(
                                              "Description : ${_description}");
                                        });
                                      },
                                    ),
                                  ),

                                  //------------------

                                  Container(
                                    margin: EdgeInsets.only(top: 10),
                                    child: CompalintImgCardWidget(
                                      onRemovePressed: () {
                                        // Handle the remove image action here

                                        setState(() {
                                          filePath = ''; // Set to empty string
                                        });
                                      },
                                      licenseImage: filePath,
                                      function: () {
                                        showCustomDialog(context);
                                      },
                                      imageText: 'Upload Image',
                                      customImage:
                                          'asserts/images/addstaff.png',
                                      ftSize: scWidth / 8,
                                    ),
                                  ),

                                  //-------------------

                                  //---------------------
                                ],
                              ),
                            ),
                          ),
                        ),
                        Positioned(
                          bottom: 0,
                          left: 0,
                          right: 0,
                          child: Container(
                            margin: EdgeInsets.only(
                              top: 10,
                            ),
                            decoration: BoxDecoration(
                                // gradient: lgBlue,
                                color:
                                    filePath.isEmpty ? lightappcolor : appcolor,
                                borderRadius: BorderRadius.circular(20)),
                            width: scWidth,
                            child: ElevatedButton(
                              onPressed: () async {
                                if (_formKey.currentState!.validate()) {
                                  Random random = Random();

                                  int randomId = random.nextInt(1000);
                                  Map<String, dynamic> complaintData = {
                                    'tagId': randomId,
                                    'tag': "Complaint",
                                    'status_id': _statusId.toString(),
                                    'category_id': _catID.toString(),
                                    'subcategory_id': _subCatID.toString(),
                                    'area_id': _areaId.toString(),
                                    'description': _description.toString(),
                                    'latitude': latitude.toString(),
                                    'longitude': longitude.toString(),
                                    'attachments': filePath,
                                  };
                                  bool internetConnected =
                                      await isInternetConnected();
                                  if (internetConnected) {
                                    setState(() {
                                      _isLoading = true;
                                    });

                                    if (filePath.isEmpty) {
                                      _isLoading = false;
                                      funToast("Image is Required", appcolor);
                                    } else {
                                      setState(() {
                                        _isLoading = true;
                                      });
                                      postComplaintData(); // Call your function to post the complaint
                                    }
                                  } else {
                                    /////
                                    // ComplaintLocalModel newComplaint =
                                    //     ComplaintLocalModel(
                                    //   statusId: _statusId.toString(),
                                    //   categoryId: _catID.toString(),
                                    //   subcategoryId: _subCatID.toString(),
                                    //   areaId: _areaId.toString(),
                                    //   description: _description.toString(),
                                    //   latitude: latitude.toString(),
                                    //   longitude: longitude.toString(),
                                    //   attachments: filePath,
                                    // );
                                    // // Use the toMap method if you need to convert it to a map
                                    // final Map<String, dynamic> complaintMap =
                                    //     newComplaint.toMap();
                                    if (filePath.isEmpty) {
                                      _isLoading = false;
                                      funToast("Image is Required", appcolor);
                                    } else {
                                      setState(() {
                                        _isLoading = true;
                                      });
                                      await enqueueComplaint(
                                          complaintData); // Call your function to post the complaint
                                    }

                                    // showAnimatedCheckmarkDialog(
                                    //     context,
                                    //     'No internet connectivity!\nComplaint Stored in Pending Task!',
                                    //     appcolor);
                                    // _isLoading = false;
                                    // await Future.delayed(Duration(seconds: 1));

                                    print(
                                        'No internet connectivity. Complaint enqueued.');

                                    // Navigate to the dashboard
                                  }
                                }
                              },
                              child: Text(
                                'Submit',
                                style: TextStyle(color: btnTextColor),
                              ),
                              style: ElevatedButton.styleFrom(
                                elevation: 0,
                                backgroundColor: Colors.transparent,
                                padding: EdgeInsets.symmetric(vertical: 12),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(roundBtn),
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
