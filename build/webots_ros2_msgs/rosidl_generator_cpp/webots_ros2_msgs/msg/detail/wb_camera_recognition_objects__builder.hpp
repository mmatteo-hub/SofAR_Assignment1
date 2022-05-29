// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from webots_ros2_msgs:msg/WbCameraRecognitionObjects.idl
// generated code does not contain a copyright notice

#ifndef WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECTS__BUILDER_HPP_
#define WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECTS__BUILDER_HPP_

#include "webots_ros2_msgs/msg/detail/wb_camera_recognition_objects__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace webots_ros2_msgs
{

namespace msg
{

namespace builder
{

class Init_WbCameraRecognitionObjects_objects
{
public:
  explicit Init_WbCameraRecognitionObjects_objects(::webots_ros2_msgs::msg::WbCameraRecognitionObjects & msg)
  : msg_(msg)
  {}
  ::webots_ros2_msgs::msg::WbCameraRecognitionObjects objects(::webots_ros2_msgs::msg::WbCameraRecognitionObjects::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::webots_ros2_msgs::msg::WbCameraRecognitionObjects msg_;
};

class Init_WbCameraRecognitionObjects_header
{
public:
  Init_WbCameraRecognitionObjects_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WbCameraRecognitionObjects_objects header(::webots_ros2_msgs::msg::WbCameraRecognitionObjects::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_WbCameraRecognitionObjects_objects(msg_);
  }

private:
  ::webots_ros2_msgs::msg::WbCameraRecognitionObjects msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::webots_ros2_msgs::msg::WbCameraRecognitionObjects>()
{
  return webots_ros2_msgs::msg::builder::Init_WbCameraRecognitionObjects_header();
}

}  // namespace webots_ros2_msgs

#endif  // WEBOTS_ROS2_MSGS__MSG__DETAIL__WB_CAMERA_RECOGNITION_OBJECTS__BUILDER_HPP_
