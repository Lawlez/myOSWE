/*
 * fixedpoint.h, fixed-point math macros
 * Copyright (C) 2010 Christopher Williams
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#ifndef _FIXEDPOINT_H_
#define _FIXEDPOINT_H_

typedef long fixedpoint;

#define FIXED_SHIFT 8
#define FIXED_ONE ((fixedpoint)1<<FIXED_SHIFT)
#define FIXED_HALF ((fixedpoint)1<<(FIXED_SHIFT-1))

#define TO_FIXED(a) (fixedpoint)((a)*FIXED_ONE)
#define FIXED_I(a) (long)((a)/FIXED_ONE)
#define FIXED_F(a) (long)((a)%FIXED_ONE)
#define FIXED_DIV(a,b) (fixedpoint)(((long long)(a)*FIXED_ONE)/(b))
#define FIXED_MUL(a,b) (fixedpoint)((long long)(a)*(b)/FIXED_ONE)
#define FIXED_TO_FLOAT(a) ((float)(a)/FIXED_ONE)

#endif
