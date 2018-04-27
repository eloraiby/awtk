﻿/**
 * File:   window_manager.h
 * Author: Li XianJing <xianjimli@hotmail.com>
 * Brief:  window manager
 *
 * Copyright (c) 2018 - 2018  Li XianJing <xianjimli@hotmail.com>
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * License file for more details.
 *
 */

/**
 * History:
 * ================================================================
 * 2018-01-13 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#ifndef TK_WINDOW_MANAGER_H
#define TK_WINDOW_MANAGER_H

#include "base/widget.h"
#include "base/canvas.h"
#include "base/window_animator.h"

BEGIN_C_DECLS

/**
 * @class window_manager_t
 * @parent widget_t
 * 窗口管理器。
 */
typedef struct _window_manager_t {
  widget_t widget;

  array_t graps;
  rect_t dirty_rect;
  rect_t last_dirty_rect;

  uint8_t ctrl : 1;
  uint8_t alt : 1;
  uint8_t shift : 1;
  uint8_t caplock : 1;
  point_t pointer;

  bool_t animating;
  bool_t ignore_user_input;
  window_animator_t* animator;
  canvas_t* canvas;
} window_manager_t;

widget_t* window_manager(void);

widget_t* window_manager_init(window_manager_t* wm);

widget_t* window_manager_get_top_window(widget_t* widget);
ret_t window_manager_resize(widget_t* wm, wh_t w, wh_t h);
ret_t window_manager_add_child(widget_t* wm, widget_t* window);
ret_t window_manager_remove_child(widget_t* wm, widget_t* window);
ret_t window_manager_paint(widget_t* wm, canvas_t* c);
ret_t window_manager_dispatch_input_event(widget_t* wm, event_t* e);

ret_t window_manager_set_animating(widget_t* wm, bool_t animating);

#define WINDOW_MANAGER(widget) ((window_manager_t*)(widget))

END_C_DECLS

#endif /*TK_WINDOW_MANAGER_H*/
