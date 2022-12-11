fn soma(x: i32, y: i32) -> i32 {
var a: i32;
a = x + y;
Print(a);
return a;
}
fn Main() {
var c: i32;
var b: i32;
c = 3;
b = soma(c, 4);
Print(c);
Print(b);
}