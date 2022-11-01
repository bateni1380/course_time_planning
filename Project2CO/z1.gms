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
         k 
         p(i,h)
         s(j,c)
         n(c)
         a(c,l)
         b(l,d,h);
$GDXIN %gdxincname%
$LOAD p,s,n,a,b,k
$GDXIN

nonnegative variable w;
variable z1;
binary variable delta(c,d,h);

equation obj, const1, const2, const3, const4, const5, const6,
 constz1;


obj..
         z1=e=w;
         
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

         
model problem /all/;
solve problem using MIP minimizing z1;
display z1.l, delta.l,p,c,l,d,h,j,s,n,a,b;


parameter
    stat;
stat = problem.modelStat;
display stat