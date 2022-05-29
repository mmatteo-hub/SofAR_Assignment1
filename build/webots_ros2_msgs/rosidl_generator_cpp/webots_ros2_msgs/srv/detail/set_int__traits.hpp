// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from webots_ros2_msgs:srv/SetInt.idl
// generated code does not contain a copyright notice

#ifndef WEBOTS_ROS2_MSGS__SRV__DETAIL__SET_INT__TRAITS_HPP_
#define WEBOTS_ROS2_MSGS__SRV__DETAIL__SET_INT__TRAITS_HPP_

#include "webots_ros2_msgs/srv/detail/set_int__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

namespace rosidl_generator_traits
{

inline void to_yaml(
  const webots_ros2_msgs::srv::SetInt_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value: ";
    value_to_yaml(msg.value, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const webots_ros2_msgs::srv::SetInt_Request & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<webots_ros2_msgs::srv::SetInt_Request>()
{
  return "webots_ros2_msgs::srv::SetInt_Request";
}

template<>
inline const char * name<webots_ros2_msgs::srv::SetInt_Request>()
{
  return "webots_ros2_msgs/srv/SetInt_Request";
}

template<>
struct has_fixed_size<webots_ros2_msgs::srv::SetInt_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<webots_ros2_msgs::srv::SetInt_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<webots_ros2_msgs::srv::SetInt_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

inline void to_yaml(
  const webots_ros2_msgs::srv::SetInt_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const webots_ros2_msgs::srv::SetInt_Response & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<webots_ros2_msgs::srv::SetInt_Response>()
{
  return "webots_ros2_msgs::srv::SetInt_Response";
}

template<>
inline const char * name<webots_ros2_msgs::srv::SetInt_Response>()
{
  return "webots_ros2_msgs/srv/SetInt_Response";
}

template<>
struct has_fixed_size<webots_ros2_msgs::srv::SetInt_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<webots_ros2_msgs::srv::SetInt_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<webots_ros2_msgs::srv::SetInt_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<webots_ros2_msgs::srv::SetInt>()
{
  return "webots_ros2_msgs::srv::SetInt";
}

template<>
inline const char * name<webots_ros2_msgs::srv::SetInt>()
{
  return "webots_ros2_msgs/srv/SetInt";
}

template<>
struct has_fixed_size<webots_ros2_msgs::srv::SetInt>
  : std::integral_constant<
    bool,
    has_fixed_size<webots_ros2_msgs::srv::SetInt_Request>::value &&
    has_fixed_size<webots_ros2_msgs::srv::SetInt_Response>::value
  >
{
};

template<>
struct has_bounded_size<webots_ros2_msgs::srv::SetInt>
  : std::integral_constant<
    bool,
    has_bounded_size<webots_ros2_msgs::srv::SetInt_Request>::value &&
    has_bounded_size<webots_ros2_msgs::srv::SetInt_Response>::value
  >
{
};

template<>
struct is_service<webots_ros2_msgs::srv::SetInt>
  : std::true_type
{
};

template<>
struct is_service_request<webots_ros2_msgs::srv::SetInt_Request>
  : std::true_type
{
};

template<>
struct is_service_response<webots_ros2_msgs::srv::SetInt_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // WEBOTS_ROS2_MSGS__SRV__DETAIL__SET_INT__TRAITS_HPP_
