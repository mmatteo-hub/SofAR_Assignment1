// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from webots_ros2_msgs:srv/SetInt.idl
// generated code does not contain a copyright notice
#include "webots_ros2_msgs/srv/detail/set_int__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

bool
webots_ros2_msgs__srv__SetInt_Request__init(webots_ros2_msgs__srv__SetInt_Request * msg)
{
  if (!msg) {
    return false;
  }
  // value
  return true;
}

void
webots_ros2_msgs__srv__SetInt_Request__fini(webots_ros2_msgs__srv__SetInt_Request * msg)
{
  if (!msg) {
    return;
  }
  // value
}

bool
webots_ros2_msgs__srv__SetInt_Request__are_equal(const webots_ros2_msgs__srv__SetInt_Request * lhs, const webots_ros2_msgs__srv__SetInt_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // value
  if (lhs->value != rhs->value) {
    return false;
  }
  return true;
}

bool
webots_ros2_msgs__srv__SetInt_Request__copy(
  const webots_ros2_msgs__srv__SetInt_Request * input,
  webots_ros2_msgs__srv__SetInt_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // value
  output->value = input->value;
  return true;
}

webots_ros2_msgs__srv__SetInt_Request *
webots_ros2_msgs__srv__SetInt_Request__create()
{
  webots_ros2_msgs__srv__SetInt_Request * msg = (webots_ros2_msgs__srv__SetInt_Request *)malloc(sizeof(webots_ros2_msgs__srv__SetInt_Request));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(webots_ros2_msgs__srv__SetInt_Request));
  bool success = webots_ros2_msgs__srv__SetInt_Request__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
webots_ros2_msgs__srv__SetInt_Request__destroy(webots_ros2_msgs__srv__SetInt_Request * msg)
{
  if (msg) {
    webots_ros2_msgs__srv__SetInt_Request__fini(msg);
  }
  free(msg);
}


bool
webots_ros2_msgs__srv__SetInt_Request__Sequence__init(webots_ros2_msgs__srv__SetInt_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  webots_ros2_msgs__srv__SetInt_Request * data = NULL;
  if (size) {
    data = (webots_ros2_msgs__srv__SetInt_Request *)calloc(size, sizeof(webots_ros2_msgs__srv__SetInt_Request));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = webots_ros2_msgs__srv__SetInt_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        webots_ros2_msgs__srv__SetInt_Request__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
webots_ros2_msgs__srv__SetInt_Request__Sequence__fini(webots_ros2_msgs__srv__SetInt_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      webots_ros2_msgs__srv__SetInt_Request__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

webots_ros2_msgs__srv__SetInt_Request__Sequence *
webots_ros2_msgs__srv__SetInt_Request__Sequence__create(size_t size)
{
  webots_ros2_msgs__srv__SetInt_Request__Sequence * array = (webots_ros2_msgs__srv__SetInt_Request__Sequence *)malloc(sizeof(webots_ros2_msgs__srv__SetInt_Request__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = webots_ros2_msgs__srv__SetInt_Request__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
webots_ros2_msgs__srv__SetInt_Request__Sequence__destroy(webots_ros2_msgs__srv__SetInt_Request__Sequence * array)
{
  if (array) {
    webots_ros2_msgs__srv__SetInt_Request__Sequence__fini(array);
  }
  free(array);
}

bool
webots_ros2_msgs__srv__SetInt_Request__Sequence__are_equal(const webots_ros2_msgs__srv__SetInt_Request__Sequence * lhs, const webots_ros2_msgs__srv__SetInt_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!webots_ros2_msgs__srv__SetInt_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
webots_ros2_msgs__srv__SetInt_Request__Sequence__copy(
  const webots_ros2_msgs__srv__SetInt_Request__Sequence * input,
  webots_ros2_msgs__srv__SetInt_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(webots_ros2_msgs__srv__SetInt_Request);
    webots_ros2_msgs__srv__SetInt_Request * data =
      (webots_ros2_msgs__srv__SetInt_Request *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!webots_ros2_msgs__srv__SetInt_Request__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          webots_ros2_msgs__srv__SetInt_Request__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!webots_ros2_msgs__srv__SetInt_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
webots_ros2_msgs__srv__SetInt_Response__init(webots_ros2_msgs__srv__SetInt_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  return true;
}

void
webots_ros2_msgs__srv__SetInt_Response__fini(webots_ros2_msgs__srv__SetInt_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
}

bool
webots_ros2_msgs__srv__SetInt_Response__are_equal(const webots_ros2_msgs__srv__SetInt_Response * lhs, const webots_ros2_msgs__srv__SetInt_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  return true;
}

bool
webots_ros2_msgs__srv__SetInt_Response__copy(
  const webots_ros2_msgs__srv__SetInt_Response * input,
  webots_ros2_msgs__srv__SetInt_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  return true;
}

webots_ros2_msgs__srv__SetInt_Response *
webots_ros2_msgs__srv__SetInt_Response__create()
{
  webots_ros2_msgs__srv__SetInt_Response * msg = (webots_ros2_msgs__srv__SetInt_Response *)malloc(sizeof(webots_ros2_msgs__srv__SetInt_Response));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(webots_ros2_msgs__srv__SetInt_Response));
  bool success = webots_ros2_msgs__srv__SetInt_Response__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
webots_ros2_msgs__srv__SetInt_Response__destroy(webots_ros2_msgs__srv__SetInt_Response * msg)
{
  if (msg) {
    webots_ros2_msgs__srv__SetInt_Response__fini(msg);
  }
  free(msg);
}


bool
webots_ros2_msgs__srv__SetInt_Response__Sequence__init(webots_ros2_msgs__srv__SetInt_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  webots_ros2_msgs__srv__SetInt_Response * data = NULL;
  if (size) {
    data = (webots_ros2_msgs__srv__SetInt_Response *)calloc(size, sizeof(webots_ros2_msgs__srv__SetInt_Response));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = webots_ros2_msgs__srv__SetInt_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        webots_ros2_msgs__srv__SetInt_Response__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
webots_ros2_msgs__srv__SetInt_Response__Sequence__fini(webots_ros2_msgs__srv__SetInt_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      webots_ros2_msgs__srv__SetInt_Response__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

webots_ros2_msgs__srv__SetInt_Response__Sequence *
webots_ros2_msgs__srv__SetInt_Response__Sequence__create(size_t size)
{
  webots_ros2_msgs__srv__SetInt_Response__Sequence * array = (webots_ros2_msgs__srv__SetInt_Response__Sequence *)malloc(sizeof(webots_ros2_msgs__srv__SetInt_Response__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = webots_ros2_msgs__srv__SetInt_Response__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
webots_ros2_msgs__srv__SetInt_Response__Sequence__destroy(webots_ros2_msgs__srv__SetInt_Response__Sequence * array)
{
  if (array) {
    webots_ros2_msgs__srv__SetInt_Response__Sequence__fini(array);
  }
  free(array);
}

bool
webots_ros2_msgs__srv__SetInt_Response__Sequence__are_equal(const webots_ros2_msgs__srv__SetInt_Response__Sequence * lhs, const webots_ros2_msgs__srv__SetInt_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!webots_ros2_msgs__srv__SetInt_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
webots_ros2_msgs__srv__SetInt_Response__Sequence__copy(
  const webots_ros2_msgs__srv__SetInt_Response__Sequence * input,
  webots_ros2_msgs__srv__SetInt_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(webots_ros2_msgs__srv__SetInt_Response);
    webots_ros2_msgs__srv__SetInt_Response * data =
      (webots_ros2_msgs__srv__SetInt_Response *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!webots_ros2_msgs__srv__SetInt_Response__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          webots_ros2_msgs__srv__SetInt_Response__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!webots_ros2_msgs__srv__SetInt_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
