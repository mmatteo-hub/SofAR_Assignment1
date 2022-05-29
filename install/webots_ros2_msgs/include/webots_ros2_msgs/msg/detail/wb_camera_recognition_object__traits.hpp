// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from webots_ros2_msgs:msg/WbCameraRecognitionObject.idl
// generated code does not contain a copyright notice

#ifndef WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECT__TRAITS_HPP_
#define WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECT__TRAITS_HPP_

#include "webots_ros2_msgs/msg/detail/wb_camera_recognition_object__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

// Include directives for member types
// Member 'pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"
// Member 'bbox'
#include "vision_msgs/msg/detail/bounding_box2_d__traits.hpp"
// Member 'colors'
#include "std_msgs/msg/detail/color_rgba__traits.hpp"

namespace rosidl_generator_traits
{

inline void to_yaml(
  const webots_ros2_msgs::msg::WbCameraRecognitionObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_yaml(msg.pose, out, indentation + 2);
  }

  // member: bbox
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bbox:\n";
    to_yaml(msg.bbox, out, indentation + 2);
  }

  // member: colors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.colors.size() == 0) {
      out << "colors: []\n";
    } else {
      out << "colors:\n";
      for (auto item : msg.colors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: model
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "model: ";
    value_to_yaml(msg.model, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const webots_ros2_msgs::msg::WbCameraRecognitionObject & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<webots_ros2_msgs::msg::WbCameraRecognitionObject>()
{
  return "webots_ros2_msgs::msg::WbCameraRecognitionObject";
}

template<>
inline const char * name<webots_ros2_msgs::msg::WbCameraRecognitionObject>()
{
  return "webots_ros2_msgs/msg/WbCameraRecognitionObject";
}

template<>
struct has_fixed_size<webots_ros2_msgs::msg::WbCameraRecognitionObject>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<webots_ros2_msgs::msg::WbCameraRecognitionObject>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<webots_ros2_msgs::msg::WbCameraRecognitionObject>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECT__TRAITS_HPP_
