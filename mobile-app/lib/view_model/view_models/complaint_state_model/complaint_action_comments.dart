class ComplaintActionCommentsDataModel {
  final int status;
  final String message;
  final List<ComplaintActionCommentsItemModel> dataArray;
  ComplaintActionCommentsDataModel({
    required this.status,
    required this.message,
    required this.dataArray,
  });
  factory ComplaintActionCommentsDataModel.fromJson(Map<String, dynamic> json) {
    List<dynamic> data = json['data_array'];
    List<ComplaintActionCommentsItemModel> dataArray =
        data.map((item) => ComplaintActionCommentsItemModel.fromJson(item)).toList();
    return ComplaintActionCommentsDataModel(
      status: json['status'],
      message: json['message'],
      dataArray: dataArray,
    );
  }
  Map<String, dynamic> toJson() {
    List<Map<String, dynamic>> dataArrayJson =
        dataArray.map((item) => item.toJson()).toList();
    return {
      'status': status,
      'message': message,
      'data_array': dataArrayJson,
    };
  }
}
class ComplaintActionCommentsItemModel {
  final String? id;
  final String? uid;
  final String? status;
  final String? color;
  final double? progress;
  final String? createdOn;
  final String? updatedOn;
  final String? ip;
  final String? serialNumber;
  final bool? reply;
  final String? comment;
  final String? tagTime;
  final bool? tagSeen;
  final String? latitude;
  final String? longitude;
  final String createdBy;
  final String? updatedBy;
  final String? parent;
  final String? complaint;
  final String? complaintAction;
  final String? tagTo;
  final String? tagFrom;
  ComplaintActionCommentsItemModel({
    required this.id,
    required this.uid,
    required this.status,
    required this.color,
    required this.progress,
    required this.createdOn,
    required this.updatedOn,
    required this.ip,
    required this.serialNumber,
    required this.reply,
    required this.comment,
    required this.tagTime,
    required this.tagSeen,
    required this.latitude,
    required this.longitude,
    required this.createdBy,
    required this.updatedBy,
    required this.parent,
    required this.complaint,
    required this.complaintAction,
    required this.tagTo,
    required this.tagFrom,
  });
  factory ComplaintActionCommentsItemModel.fromJson(Map<String, dynamic> json) {
    return ComplaintActionCommentsItemModel(
      id: json['id'],
      uid: json['uid'],
      status: json['status'],
      color: json['color'],
      progress: json['progress'].toDouble(),
      createdOn: json['created_on'],
      updatedOn: json['updated_on'],
      ip: json['ip'],
      serialNumber: json['serial_number'],
      reply: json['reply'],
      comment: json['comment'],
      tagTime: json['tag_time'],
      tagSeen: json['tag_seen'],
      latitude: json['latitude'],
      longitude: json['longitude'],
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      parent: json['parent'],
      complaint: json['complaint'],
      complaintAction: json['complaint_action'],
      tagTo: json['tag_to'],
      tagFrom: json['tag_from'],
    );
  }
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'uid': uid,
      'status': status,
      'color': color,
      'progress': progress,
      'created_on': createdOn,
      'updated_on': updatedOn,
      'ip': ip,
      'serial_number': serialNumber,
      'reply': reply,
      'comment': comment,
      'tag_time': tagTime,
      'tag_seen': tagSeen,
      'latitude': latitude,
      'longitude': longitude,
      'created_by': createdBy,
      'updated_by': updatedBy,
      'parent': parent,
      'complaint': complaint,
      'complaint_action': complaintAction,
      'tag_to': tagTo,
      'tag_from': tagFrom,
    };
  }
}




// class ComplaintActionCommentsDataModel {
//   final int status;
//   final String message;
//   final CommentsDataArray dataArray;

//   ComplaintActionCommentsDataModel({
//     required this.status,
//     required this.message,
//     required this.dataArray,
//   });

//   factory ComplaintActionCommentsDataModel.fromJson(Map<String, dynamic> json) {
//     return ComplaintActionCommentsDataModel(
//       status: json['status'],
//       message: json['message'],
//       dataArray: CommentsDataArray.fromJson(json['data_array']),
//     );
//   }
// }

// class CommentsDataArray {
//   final ComplaintActionComments complaintActionComments;
//   final List<Comment> comments;

//   CommentsDataArray({
//     required this.complaintActionComments,
//     required this.comments,
//   });

//   factory CommentsDataArray.fromJson(Map<String, dynamic> json) {
//     return CommentsDataArray(
//       complaintActionComments: ComplaintActionComments.fromJson(json['complaint_action_comments']),
//       comments: List<Comment>.from(
//         json['comments'].map(
//           (comment) => Comment.fromJson(comment),
//         ),
//       ),
//     );
//   }
// }

// class ComplaintActionComments {
//   final String actionId;
//   final String uid;
//   final String status;
//   final String color;

//   ComplaintActionComments({
//     required this.actionId,
//     required this.uid,
//     required this.status,
//     required this.color,
//   });

//   factory ComplaintActionComments.fromJson(Map<String, dynamic> json) {
//     return ComplaintActionComments(
//       actionId: json['action_id'],
//       uid: json['uid'],
//       status: json['status'],
//       color: json['color'],
//     );
//   }
// }

// class Comment {
//   final String id;
//   final String uid;
//   final String text;
//   final String createdBy;
//   final String createdAt;

//   Comment({
//     required this.id,
//     required this.uid,
//     required this.text,
//     required this.createdBy,
//     required this.createdAt,
//   });

//   factory Comment.fromJson(Map<String, dynamic> json) {
//     return Comment(
//       id: json['id'] ?? "",
//       uid: json['uid'] ?? "",
//       text: json['text'] ?? "",
//       createdBy: json['created_by'] ?? "",
//       createdAt: json['created_at'] ?? "",
//     );
//   }
// }

// Map<String, dynamic> complaintActionCommentsModelToJson(ComplaintActionCommentsDataModel model) {
//   return {
//     'status': model.status,
//     'message': model.message,
//     'data_array': commentsDataArrayToJson(model.dataArray),
//   };
// }

// Map<String, dynamic> commentsDataArrayToJson(CommentsDataArray dataArray) {
//   return {
//     'complaint_action_comments': complaintActionCommentsToJson(dataArray.complaintActionComments),
//     'comments': dataArray.comments
//         .map((comment) => commentToJson(comment))
//         .toList(),
//   };
// }

// Map<String, dynamic> complaintActionCommentsToJson(ComplaintActionComments complaintActionComments) {
//   return {
//     'action_id': complaintActionComments.actionId,
//     'uid': complaintActionComments.uid,
//     'status': complaintActionComments.status,
//     'color': complaintActionComments.color,
//   };
// }

// Map<String, dynamic> commentToJson(Comment comment) {
//   return {
//     'id': comment.id,
//     'uid': comment.uid,
//     'text': comment.text,
//     'created_by': comment.createdBy,
//     'created_at': comment.createdAt,
//   };
// }
