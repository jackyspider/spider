# 操作函数模块operator

- 这个模块为常规的python运算操作符提供了对应的函数。
- 各函数本身功能与运算符一致，但在一些特殊情况下依然需要调用这个模块。
- 调用情况常见于使用某些迭代器中。

操作函数模块operator

- [常用对照速查表](https://blog.csdn.net/weixin_41084236/article/details/81509339#%E5%B8%B8%E7%94%A8%E5%AF%B9%E7%85%A7%E9%80%9F%E6%9F%A5%E8%A1%A8)

- 成员介绍

  - [特殊操作](https://blog.csdn.net/weixin_41084236/article/details/81509339#%E7%89%B9%E6%AE%8A%E6%93%8D%E4%BD%9C)

  - [数值运算](https://blog.csdn.net/weixin_41084236/article/details/81509339#%E6%95%B0%E5%80%BC%E8%BF%90%E7%AE%97)

  - [赋值运算](https://blog.csdn.net/weixin_41084236/article/details/81509339#%E8%B5%8B%E5%80%BC%E8%BF%90%E7%AE%97)

  - [比较运算](https://blog.csdn.net/weixin_41084236/article/details/81509339#%E6%AF%94%E8%BE%83%E8%BF%90%E7%AE%97)

  - [逻辑运算](https://blog.csdn.net/weixin_41084236/article/details/81509339#%E9%80%BB%E8%BE%91%E8%BF%90%E7%AE%97)

    

## 常用对照速查表

<div class="table-box"><table>
<thead>
<tr>
  <th align="center">实际操作</th>
  <th align="center">运算符</th>
  <th align="center">对应函数</th>
</tr>
</thead>
<tbody><tr>
  <td align="center">加</td>
  <td align="center">a + b</td>
  <td align="center">add(a, b)</td>
</tr>
<tr>
  <td align="center">串联列表</td>
  <td align="center">seq1 + seq2</td>
  <td align="center">concat(seq1, seq2)</td>
</tr>
<tr>
  <td align="center">查询包含</td>
  <td align="center">obj in seq</td>
  <td align="center">contains(seq, obj)</td>
</tr>
<tr>
  <td align="center">除</td>
  <td align="center">a / b</td>
  <td align="center">truediv(a, b)</td>
</tr>
<tr>
  <td align="center">除</td>
  <td align="center">a // b</td>
  <td align="center">floordiv(a, b)</td>
</tr>
<tr>
  <td align="center">位与</td>
  <td align="center">a &amp; b</td>
  <td align="center">and_(a, b)</td>
</tr>
<tr>
  <td align="center">位异或</td>
  <td align="center">a ^ b</td>
  <td align="center">xor(a, b)</td>
</tr>
<tr>
  <td align="center">位反</td>
  <td align="center">~ a</td>
  <td align="center">invert(a)</td>
</tr>
<tr>
  <td align="center">位或</td>
  <td align="center">a | b</td>
  <td align="center">or_(a, b)</td>
</tr>
<tr>
  <td align="center">指数</td>
  <td align="center">a ** b</td>
  <td align="center">pow(a, b)</td>
</tr>
<tr>
  <td align="center">判断</td>
  <td align="center">a is b</td>
  <td align="center">is_(a, b)</td>
</tr>
<tr>
  <td align="center">判断</td>
  <td align="center">a is not b</td>
  <td align="center">is_not(a, b)</td>
</tr>
<tr>
  <td align="center">索引赋值</td>
  <td align="center">obj[k] = v</td>
  <td align="center">setitem(obj, k, v)</td>
</tr>
<tr>
  <td align="center">索引删除</td>
  <td align="center">del obj[k]</td>
  <td align="center">delitem(obj, k)</td>
</tr>
<tr>
  <td align="center">索引查询</td>
  <td align="center">obj[k]</td>
  <td align="center">getitem(obj, k)</td>
</tr>
<tr>
  <td align="center">位左移</td>
  <td align="center">a &lt;&lt; b</td>
  <td align="center">lshift(a, b)</td>
</tr>
<tr>
  <td align="center">模</td>
  <td align="center">a % b</td>
  <td align="center">mod(a, b)</td>
</tr>
<tr>
  <td align="center">乘</td>
  <td align="center">a * b</td>
  <td align="center">mul(a, b)</td>
</tr>
<tr>
  <td align="center">矩阵乘（存在bug）</td>
  <td align="center">a @ b</td>
  <td align="center">matmul(a, b)</td>
</tr>
<tr>
  <td align="center">算数取反</td>
  <td align="center">-a</td>
  <td align="center">neg(a)</td>
</tr>
<tr>
  <td align="center">逻辑取反</td>
  <td align="center">not a</td>
  <td align="center">not_(a)</td>
</tr>
<tr>
  <td align="center">取正</td>
  <td align="center">+a</td>
  <td align="center">pos(a)</td>
</tr>
<tr>
  <td align="center">位右移</td>
  <td align="center">a &gt;&gt; b</td>
  <td align="center">rshift(a, b)</td>
</tr>
<tr>
  <td align="center">切片赋值</td>
  <td align="center">seq[i:j] = values</td>
  <td align="center">setitem(seq, slice(i, j), values)</td>
</tr>
<tr>
  <td align="center">切片删除</td>
  <td align="center">del seq[i:j]</td>
  <td align="center">delitem(seq, slice(i, j))</td>
</tr>
<tr>
  <td align="center">切片</td>
  <td align="center">seq[i:j]</td>
  <td align="center">getitem(seq, slice(i, j))</td>
</tr>
<tr>
  <td align="center">格式化字符串</td>
  <td align="center">s % obj</td>
  <td align="center">mod(s, obj)</td>
</tr>
<tr>
  <td align="center">减</td>
  <td align="center">a - b</td>
  <td align="center">sub(a, b)</td>
</tr>
<tr>
  <td align="center">为真检验</td>
  <td align="center">obj</td>
  <td align="center">truth(obj)</td>
</tr>
<tr>
  <td align="center">大小判断</td>
  <td align="center">a &lt; b</td>
  <td align="center">lt(a, b)</td>
</tr>
<tr>
  <td align="center">大小判断</td>
  <td align="center">a &lt;= b</td>
  <td align="center">le(a, b)</td>
</tr>
<tr>
  <td align="center">相等判断</td>
  <td align="center">a == b</td>
  <td align="center">eq(a, b)</td>
</tr>
<tr>
  <td align="center">不等判断</td>
  <td align="center">a != b</td>
  <td align="center">ne(a, b)</td>
</tr>
<tr>
  <td align="center">大小判断</td>
  <td align="center">a &gt;= b</td>
  <td align="center">ge(a, b)</td>
</tr>
<tr>
  <td align="center">大小判断</td>
  <td align="center">a &gt; b</td>
  <td align="center">gt(a, b)</td>
</tr>
</tbody></table></div>

### 特殊操作

**operator.attrgetter(attr)** 
**operator.attrgetter(\*attrs)**

- 调用操作（.）

>>> from operator import *
>>> import math
>>> a=attrgetter('pi')
>>> a(math)
>>> 3.141592653589793
>>> b=attrgetter('pi','e')
>>> b(math)
>>> (3.141592653589793, 2.718281828459045)
**operator.methodcaller(name[, args…])**

可带参数的attrgetter 

After f = methodcaller(‘name’), the call f(b) returns b.name(). 

After f = methodcaller(‘name’, ‘foo’, bar=1), the call f(b) returns b.name(‘foo’, bar=1).



operator.index(a)

* 返回整数a

operator.concat(a, b)

* 串联列表

operator.delitem(a, b)

* 列表删除元素

operator.getitem(a, b)

* 索引查询

operator.indexOf(a, b)

* 查询索引

operator.setitem(a, b, c)

* 索引赋值

operator.length_hint(obj, default=0)

* 长度查询

### 数值运算

operator.abs(obj)

* 取绝对值

operator.add(a, b)

* a + b

operator.and_(a, b)

* 按位与

operator.floordiv(a, b)

* a // b

operator.inv(obj) 
operator.invert(obj)

* 按位取反

operator.lshift(a, b)

* 位左移

operator.mod(a, b)

* a % b

operator.mul(a, b)

* a * b

operator.matmul(a, b)

* a @ b

operator.neg(obj)

* 取负

operator.or_(a, b)

* 按位或

operator.pos(obj)

* 取正

operator.pow(a, b)

* a ** b

operator.rshift(a, b)

* 位右移

operator.sub(a, b)

* a - b

operator.truediv(a, b)

* 浮点除

operator.xor(a, b)

* 按位异或

## 赋值运算

operator.iadd(a, b)

* a = iadd(a, b) 等于 a += b

operator.iand(a, b)

* a = iand(a, b) 等于 a &= b.

operator.iconcat(a, b)

* a = iconcat(a, b) 等于 a += b，ab皆为列表.

operator.ifloordiv(a, b)

* a = ifloordiv(a, b) 等于 a //= b.

operator.ilshift(a, b)

* a = ilshift(a, b) 等于 a <<= b.

operator.imod(a, b)

* a = imod(a, b) 等于 a %= b.

operator.imul(a, b)

* a = imul(a, b) 等于 a *= b.

operator.imatmul(a, b)

* a = imatmul(a, b) 等于 a @= b.

operator.ior(a, b)

* a = ior(a, b) 等于 a |= b.

operator.ipow(a, b)

* a = ipow(a, b) 等于 a **= b.

operator.irshift(a, b)

* a = irshift(a, b) 等于 a >>= b.

operator.isub(a, b)

* a = isub(a, b) 等于 a -= b.

operator.itruediv(a, b)

* a = itruediv(a, b) 等于 a /= b.

operator.ixor(a, b)

* a = ixor(a, b) 等于 a ^= b.

## 比较运算

operator.lt(a, b)

* 等于 a < b

operator.le(a, b)

* 等于 a <= b

operator.eq(a, b)

* 等于 a == b

operator.ne(a, b)

* 等于 a != b

operator.ge(a, b)

* 等于 a >= b

operator.gt(a, b)

* 等于 a > b

## 逻辑运算

operator.not_(obj)

逻辑取反
operator.truth(obj)

真伪判断
operator.is_(a, b)

等同判断
operator.is_not(a, b)

不等判断
operator.contains(a, b)

包含判断
operator.countOf(a, b)

包含计数

