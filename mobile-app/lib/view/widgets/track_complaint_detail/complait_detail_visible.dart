import 'package:dha_ctt_app/constant.dart';
import 'package:dha_ctt_app/view/screens/complaint/track_complaint/complaint_detail_widget.dart';
import 'package:flutter/material.dart';

class ComplaintDetailVisibile extends StatefulWidget {
  final String ref;
  final String complainCat;
  final String subCat;
  final String area;
  final String status;
  final String complaintDate;
  final String percentage;
  const ComplaintDetailVisibile({
    required this.ref,
    required this.complainCat,
    required this.subCat,
    required this.area,
    required this.status,
    required this.complaintDate,
    required this.percentage,
  });

  @override
  State<ComplaintDetailVisibile> createState() =>
      _ComplaintDetailVisibileState();
}

class _ComplaintDetailVisibileState extends State<ComplaintDetailVisibile> {
  bool isComplaitDetailVisible = true;

  @override
  Widget build(BuildContext context) {
    double scWidth = MediaQuery.of(context).size.width;
    double scHeight = MediaQuery.of(context).size.height;
    return Container(
      alignment: Alignment.center,
      width: scWidth,
      margin: EdgeInsets.symmetric(vertical: marginLR, horizontal: marginLR),
      padding: EdgeInsets.symmetric(vertical: 5, horizontal: 0),
      decoration: BoxDecoration(
          color: dfColor, borderRadius: BorderRadius.circular(12)),
      child: Column(
        children: [
          Container(
            // width: scWidth / 2,
            padding: EdgeInsets.symmetric(vertical: 5),
            margin: EdgeInsets.only(left: scWidth / 6),
            // color: Colors.amber,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Text(
                  "Complaint Details",
                  style: TextStyle(
                      color: appcolor,
                      fontSize: smFontSize,
                      fontWeight: FontWeight.w600),
                ),
                InkWell(
                  onTap: () {
                    if (isComplaitDetailVisible == true) {
                      isComplaitDetailVisible = false;
                    } else {
                      isComplaitDetailVisible = true;
                    }
                    setState(() {});
                  },
                  child: Material(
                    elevation: 1,
                    color: dfColor,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(180)),
                    child: Icon(
                      isComplaitDetailVisible == true
                          ? Icons.arrow_drop_down_sharp
                          : Icons.arrow_drop_up_sharp,
                      color: appcolor,
                      size: exLgFontSize + 10,
                    ),
                  ),
                )
              ],
            ),
          ),
          Visibility(
            visible: isComplaitDetailVisible,
            child: Container(
              margin: EdgeInsets.symmetric(horizontal: 1, vertical: marginLR),
              child: Column(
                children: [
                  Material(
                    borderRadius: BorderRadius.circular(12),
                    elevation: 1,
                    child: AnimatedContainer(
                      duration: const Duration(seconds: 6),
                      curve: Curves.fastOutSlowIn,
                      padding:
                          EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Container(
                            // color: Colors.amber,
                            // width: scWidth / 2.2,
                            // height: scHeight / 4.5,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                IconTextWidget(
                                  color: appcolor,
                                  text: widget.ref,
                                  imageIcon: "asserts/images/cref.png",
                                ),
                                IconTextWidget(
                                  color: appcolor,
                                  text: widget.area,
                                  imageIcon: "asserts/ctt_icons/sector.png",
                                ),
                                IconTextWidget(
                                  color: appcolor,
                                  text: widget.status,
                                  imageIcon: "asserts/ctt_icons/status.png",
                                ),
                              ],
                            ),
                          ),
                          Container(
                            // color: Colors.amber,
                            // width: scWidth / 2.2,

                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                IconTextWidget(
                                  color: appcolor,
                                  text: widget.complainCat,
                                  imageIcon: "asserts/images/ccategory.png",
                                ),
                                IconTextWidget(
                                  color: appcolor,
                                  text: widget.subCat,
                                  imageIcon: "asserts/images/csubcategory.png",
                                ),
                                IconTextWidget(
                                  color: appcolor,
                                  text: widget.complaintDate,
                                  imageIcon: "asserts/ctt_icons/date.png",
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.only(top: 10),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Container(
                        //   margin: EdgeInsets.only(right: 15),
                        //   child: Text(
                        //     'progress',
                        //     style: TextStyle(
                        //         fontSize: dfFontSize,
                        //         fontWeight: FontWeight.w500,
                        //         color: appcolor),
                        //     overflow: TextOverflow.ellipsis,
                        //     softWrap: true,
                        //   ),
                        // ),
                        Image.asset(
                          "asserts/icons/ic_percentage.png",
                          width: scWidth / 14,
                          color: appcolor,
                        ),
                        Container(
                          margin: EdgeInsets.only(left: 15),
                          child: Text(
                            widget.percentage,
                            style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w500,
                                color: appcolor),
                            overflow: TextOverflow.ellipsis,
                            softWrap: true,
                          ),
                        ),
                      ],
                    ),
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
