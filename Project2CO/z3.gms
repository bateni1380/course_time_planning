set c    
    l    
    d    
    h    
    j    
    i;
alias(h,hp);
alias(d,dp);
alias(h,hb);
$GDXIN %gdxincname%
$LOAD i,c,l,d,j,h
$GDXIN

singleton set dd(d);
singleton set hh(h);
$GDXIN %gdxincname%
$LOAD hh,dd
$GDXIN

parameter
         z1
         z2
         k 
         p(i,h)
         s(j,c)
         n(c)
         a(c,l)
         b(l,d,h)
         ;
$GDXIN %gdxincname%
$LOAD p,s,n,a,b,k,z1,z2
$GDXIN

nonnegative variable w,v(c,d);
variable z3;
binary variable delta(c,d,h), gama(c);

equation obj1, obj2, obj3, const1, const2, const3, const4, const5, const6,
 constz1 ,constz3 ,constz2;


obj1..
         z1 =e= w;

obj2..
         z2 =e= sum(c$(n(c)>1),sum(d$(d.val < dd.val),v(c,d)));

obj3..
         z3 =e= sum(c$(n(c)>1),gama(c));
    
const1(c)..
         sum(d,sum(h,delta(c,d,h)))=e=n(c);
         
const2(d,i)..
         sum(h$(p(i,h)=1),sum(c,delta(c,d,h)))=l= k;
         
const3(d,l,i)..
         sum(h$(p(i,h)=1),sum(c$(a(c,l)=1),delta(c,d,h)))=l= 1;
         
         
const4(d,j,i)..
         sum(h$(p(i,h)=1),sum(c$(s(j,c)=1),delta(c,d,h))) =l= 1;
         
const5(c,l,d,h)$(a(c,l)=1)..
         delta(c,d,h)=l=b(l,d,h);
         
const6(c,d)$(n(c)>= 1)..
         sum(h,delta(c,d,h))=l= 1;
         
constz1..
         sum(c,sum(d,delta(c,d,hh)))-w =l= 0;

constz2(c,d)$(n(c)>1 and d.val<dd.val)..
         sum(h,delta(c,d,h)) + sum(h,delta(c,d+1,h)) - v(c,d) =l= 1;

constz3(c,d,h)$(n(c)>1)..
         sum(dp$(d.val<>dp.val),sum(hp$(h.val<>hp.val),delta(c,dp,hp) - (n(c) - 1)*gama(c))) =l= 50*(1-delta(c,d,h));


model problem /all/;
solve problem using MIP minimizing z3;
display z3.l, delta.l,p,c,l,d,h,j,s,n,a,b;


parameter
    stat;
stat = problem.modelStat;
display stat