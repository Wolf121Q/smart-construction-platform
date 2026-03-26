
import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/model/resources/values_manager.dart';
import 'package:flutter/material.dart';

import 'package:shimmer/shimmer.dart';

Widget buildShimmerIcon({
  required updatedAreaList,
  required onPressed,
}) {
  return GestureDetector(
    onTap: onPressed,
    child: Stack(
      alignment: Alignment.center,
      children: [
        Container(
          width: AppSize.s40,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: updatedAreaList ? appcolor : applightcolor, // bg color
          ),
          child: Center(
            child: Icon(
              Icons.add_location_alt_outlined,
              size: AppSize.s30,
              color: dfColor, // Change the color as needed
            ),
          ),
        ),
        if (updatedAreaList) //control shimmer effect
          Shimmer.fromColors(
            period: Duration(milliseconds: 2000),
            baseColor: Colors.transparent,
            highlightColor: Colors.white70,
            child: Container(
              alignment: Alignment.center,
              width: AppSize.s40,
              height: AppSize.s40,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(75), // Adjust as needed
                color: Colors.white, // Adjust as needed
              ),
            ),
          ),
      ],
    ),
  );
}

Widget buildAnimatedIcon() {
  return AnimatedIcon(
    icon: AnimatedIcons.view_list,
    progress: AlwaysStoppedAnimation(.48), // Adjust the progress as needed
    size: 30,
    color: appcolor,
  );
}

class ShimmerWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Shimmer.fromColors(
      baseColor: Colors.grey[300]!,
      highlightColor: Colors.grey[100]!,
      child: Container(
        margin: EdgeInsets.all(10),
        width: double.infinity,
        height: 45,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }
}

// class DottedBorderListView extends StatefulWidget {
//   final List<String> selectedAreaList;
//   final List<AreaHierarchy> updatedAreaList;
//   final int? areaId;
//   final backFun;

//   DottedBorderListView({
//     required this.selectedAreaList,
//     required this.updatedAreaList,
//     required this.areaId,
//     required this.backFun,
//   });

//   @override
//   State<DottedBorderListView> createState() => _DottedBorderListViewState();
// }

// class _DottedBorderListViewState extends State<DottedBorderListView> {
//   void removeName(int nameIndex) {
//     print(widget.updatedAreaList);
//     print(nameIndex);
//     setState(() {
//       widget.updatedAreaList.removeAt(nameIndex);
//     });
//   }

//   @override
//   Widget build(BuildContext context) {
//     double scWidth = MediaQuery.of(context).size.width;
//     double scHeight = MediaQuery.of(context).size.height;

//     return 
    
    
//     Container(
//       height: scHeight / 1.6,
//       width: scWidth,
//       child: DottedBorder(
//         borderType: BorderType.RRect,
//         strokeWidth: 1,
//         radius: Radius.circular(roundCardView),
//         color: appcolor,
//         child: Stack(
//           alignment: Alignment.center,
//           children: [
//             //Control background Image
//             if (widget.areaId == null)
//               Opacity(
//                 opacity: 0.6,
//                 child: Image.asset(
//                   "asserts/images/noarea_selection.png",
//                 ),
//               ),

//             Container(
//               padding: EdgeInsets.all(8),
//               decoration: BoxDecoration(
//                 color: Colors.transparent,
//               ),
//               child: ListView.builder(
//                 itemCount: widget.selectedAreaList.length,
//                 itemBuilder: (context, index) {
//                   double listsizer = 1.0;

//                   if (index == 0) listsizer = 1;
//                   if (index == 1) listsizer = 1.3;
//                   if (index == 2) listsizer = 1.6;
//                   if (index == 3) listsizer = 1.9;

//                   return Column(
//                     children: [
//                       Container(
//                         width: scWidth / listsizer,
//                         margin: EdgeInsets.only(
//                           top: marginSet + marginSet,
//                         ),
//                         decoration: BoxDecoration(
//                           color: appcolor,
//                           borderRadius:
//                               BorderRadius.circular(roundCardView + 10),
//                         ),
//                         child: Container(
//                             alignment: Alignment.center,
//                             padding: EdgeInsets.all(marginLR),

//                             // alignment: Alignment.center,
//                             child: Row(
//                               mainAxisAlignment: MainAxisAlignment.spaceBetween,
//                               children: [
//                                 Container(
//                                   width: scWidth / marginLR,
//                                 ),
//                                 Text(
//                                   widget.selectedAreaList[index],
//                                   style: TextStyle(
//                                       fontWeight: FontWeight.bold,
//                                       color: dfColor,
//                                       fontSize: smFontSize),
//                                   textAlign: TextAlign.center,
//                                 ),
//                                 GestureDetector(
//                                   onTap: () {
//                                     removeItemsOnIndex(index);
//                                   },
//                                   child: SizedBox(
//                                     width: scWidth / marginLR,
//                                     child: Icon(
//                                       Icons.close,
//                                       color: dfColor,
//                                       size: 25,
//                                     ),
//                                   ),
//                                 ),
//                               ],
//                             )),
//                       ),

//                       //Control the down arrow
//                       (index == widget.selectedAreaList.length - 1)
//                           ? Container()
//                           : Image.asset(
//                               "asserts/images/dropdown_polygon.png",
//                               color: appcolor,
//                               width: AppSize.s24,
//                             ),

//                       if (index == widget.selectedAreaList.length - 1)
//                         GestureDetector(
//                           onTap: () {
//                             // showDialog(
//                             //   context: context,
//                             //   builder: (BuildContext context) {
//                             //     // print("${selectedAreaList}");
//                             //     return Container(
//                             //       margin:
//                             //           EdgeInsets.only(top: 100, bottom: 100),
//                             //       child: Dialog(
//                             //         alignment: Alignment.topCenter,
//                             //         child: Container(
//                             //           padding: EdgeInsets.all(16),
//                             //           child: Column(
//                             //             mainAxisSize: MainAxisSize.min,
//                             //             children: [
//                             //               TextField(
//                             //                 controller: _controller,
//                             //                 decoration: InputDecoration(
//                             //                   labelText: 'Search',
//                             //                   hintText: 'Type to search...',
//                             //                   prefixIcon: Icon(Icons.search),
//                             //                   suffixIcon: _controller
//                             //                           .text.isNotEmpty
//                             //                       ? GestureDetector(
//                             //                           onTap: () {
//                             //                             setState(() {
//                             //                               _controller.clear();
//                             //                               selectedValue = '';
//                             //                               displayedOptions =
//                             //                                   widget.updatedAreaList;

//                             //                               print(
//                             //                                   "Step ok: ${ widget.updatedAreaList}");
//                             //                             });
//                             //                           },
//                             //                           child: Icon(Icons.clear),
//                             //                         )
//                             //                       : null,
//                             //                 ),
//                             //                 onChanged: (value) {
//                             //                   setState(() {
//                             //                     displayedOptions =
//                             //                          widget.updatedAreaList.toList();
//                             //                     // .where((option) =>
//                             //                     //     option.toLowerCase().contains(value.toLowerCase()))
//                             //                     // .toList();
//                             //                   });
//                             //                 },
//                             //               ),
//                             //               SizedBox(height: 16),
//                             //               Expanded(
//                             //                 child:  widget.updatedAreaList.isEmpty
//                             //                     ? Center(
//                             //                         child:
//                             //                             Text('Item not found'),
//                             //                       )
//                             //                     : ListView.builder(
//                             //                         itemCount:
//                             //                              widget.updatedAreaList.length,
//                             //                         itemBuilder:
//                             //                             (context, index) {
//                             //                           return ListTile(
//                             //                             title: Text(
//                             //                                widget.updatedAreaList[index]
//                             //                                   .name,
//                             //                               style: TextStyle(
//                             //                                   fontWeight:
//                             //                                       FontWeight
//                             //                                           .w500,
//                             //                                   fontSize:
//                             //                                       dfFontSize),
//                             //                             ),
//                             //                             onTap: () {
//                             //                               setState(() {
//                             //                                 selectedAreaList
//                             //                                     .add( widget.updatedAreaList[
//                             //                                             index]
//                             //                                         .name);

//                             //                                 areaId =  widget.updatedAreaList[
//                             //                                         index]
//                             //                                     .id;
//                             //                                 print('tEST iD=' +
//                             //                                     areaId
//                             //                                         .toString());

//                             //                                 print('Area Size =' +
//                             //                                      widget.updatedAreaList
//                             //                                         .length
//                             //                                         .toString());

//                             //                                 if ( widget.updatedAreaList !=
//                             //                                     null) {}
//                             //                                 getAreaFromSharedPreferences();
//                             //                               });
//                             //                               Navigator.of(context)
//                             //                                   .pop(); // Close the dialog
//                             //                             },
//                             //                           );
//                             //                         },
//                             //                       ),
//                             //               ),
//                             //               Container(
//                             //                 alignment: Alignment.centerRight,
//                             //                 child: ElevatedButton(
//                             //                   onPressed: () {
//                             //                     // Close the dialog without selecting any item
//                             //                     Navigator.of(context).pop();
//                             //                   },
//                             //                   style: ElevatedButton.styleFrom(
//                             //                     backgroundColor: appcolor,
//                             //                     elevation: 0,
//                             //                     shape: RoundedRectangleBorder(
//                             //                       borderRadius:
//                             //                           BorderRadius.circular(
//                             //                               roundBtn),
//                             //                     ),
//                             //                   ),
//                             //                   child: Text('Close'),
//                             //                 ),
//                             //               ),
//                             //             ],
//                             //           ),
//                             //         ),
//                             //       ),
//                             //     );
//                             //   },
//                             // );
//                           },
//                           child: GestureDetector(
//                             onTap:() {
//                              // Call this function where you need to show the dialog od area seletion

//                             },
//                             child: Container(
//                               margin:
//                                   EdgeInsets.symmetric(vertical: AppMargin.m20),
//                               child: Image.asset(
//                                 widget.allOptions.isEmpty
//                                     // widget.allOptions.isEmpty
//                                     ? "asserts/gifs/area_completed.gif"
//                                     : "asserts/gifs/add.gif",
//                                 color: appcolor,
//                                 width: AppSize.s60,
//                               ),
//                             ),
//                           ),
//                         ),
//                     ],
//                   );
//                 },
//               ),
//             ),
//           ],
//         ),
//       ),
//     );
 
 
//   }

//   void removeItemsOnIndex(int index) {
//     if (index >= 0 && index < widget.selectedAreaList.length) {
//       setState(() {
//         widget.selectedAreaList
//             .removeRange(index, widget.selectedAreaList.length);
//       });
//     }
//   }
// }
