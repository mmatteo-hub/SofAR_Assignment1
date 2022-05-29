// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from webots_ros2_msgs:msg/WbCameraRecognitionObjects.idl
// generated code does not contain a copyright notice

#ifndef WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECTS__TRAITS_HPP_
#define WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECTS__TRAITS_HPP_

#include "webots_ros2_msgs/msg/detail/wb_camera_recognition_objects__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'objects'
#include "webots_ros2_msgs/msg/detail/wb_camera_recognition_object__traits.hpp"

namespace rosidl_generator_traits
{

inline void to_yaml(
  const webots_ros2_msgs::msg::WbCameraRecognitionObjects & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_yaml(msg.header, out, indentation + 2);
  }

  // member: objects
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.objects.size() == 0) {
      out << "objects: []\n";
    } else {
      out << "objects:\n";
      for (auto item : msg.objects) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const webots_ros2_msgs::msg::WbCameraRecognitionObjects & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<webots_ros2_msgs::msg::WbCameraRecognitionObjects>()
{
  return "webots_ros2_msgs::msg::WbCameraRecognitionObjects";
}

template<>
inline const char * name<webots_ros2_msgs::msg::WbCameraRecognitionObjects>()
{
  return "webots_ros2_msgs/msg/WbCameraRecognitionObjects";
}

template<>
struct has_fixed_size<webots_ros2_msgs::msg::WbCameraRecognitionObjects>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<webots_ros2_msgs::msg::WbCameraRecognitionObjects>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<webots_ros2_msgs::msg::WbCameraRecognitionObjects>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECTS__TRAITS_HPP_
