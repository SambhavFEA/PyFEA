function [ vectB ] = LUSolverCP( matA, vectB )
%LUSolverCP - LU Decomposition with complete pivoting
%   Detailed explanation goes here
P=eye(size(matA,1));
Q=eye(size(matA,1));
o=int32(size(matA,1));
for i=int32(1:o)
    [r,s]=max(abs(matA(i:end,i:end)));
    [r,t]=max(r);
    s=s(t);
    if (r==0)
        error('Matrix might be singular');
    end
    if s~=1
        s=s+i-1;
        matA([i s],:)=matA([s i],:);
        P([i s],:)=P([s i],:);
    end
    if t~=1
        t=t+i-1;
        matA(:,[i t])=matA(:,[t i]);
        Q(:,[i t])=Q(:,[t i]);
    end
    for j=int32(i+1:o)
        matA(j,i)=-matA(j,i)/matA(i,i);
        for k=int32(i+1:o)
            matA(j,k)=(matA(j,i)*matA(i,k))+matA(j,k);
        end
    end
end
for i=1:o-2
    for j=1:i
        matA(o+1-j,o-1-i)=[matA(o+1-j,o-i:o-j) 1]*matA(o-i:o+1-j,o-1-i);
    end
end

vectB=P*vectB;

for i=1:o
        vectB(o+1-i)=[matA(o+1-i,1:o-i) 1]*vectB(1:o+1-i);
end

for i=1:o
    for j=1:i-1
        vectB(o+1-i)=vectB(o+1-i)-(matA(o+1-i,o+1-j)*vectB(o+1-j));
    end
    vectB(o+1-i)=vectB(o+1-i)/matA(o+1-i,o+1-i);
end

vectB=Q*vectB;
end