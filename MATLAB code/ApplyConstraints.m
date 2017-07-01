function ApplyConstraints( NodeArray,conmat,ElementArray )
%ApplyConstraints function applies constraints to objects of NodalPoints
%   Detailed explanation goes here
if isa(ElementArray,'Beam3DElement')
    eletype='Beam3d';
else
    eletype='Truss';
end
m=size(conmat,1);
for i=1:m
    switch conmat(i,1)
        case 1
            Nod=findobj(NodeArray,'No',conmat(i,2));
            for j=1:3
                if isnan(Nod.F(j)) 
                    Nod.F(j)=0;
                end
                Nod.F(j)=Nod.F(j)+conmat(i,j+2);
                if strcmp(eletype,'Beam3d')
                    if isnan(Nod.M(j)) 
                        Nod.M(j)=0; 
                    end
                    Nod.M(j)=Nod.M(j)+conmat(i,j+5);
                end
            end
        case 2
            Nod=findobj(NodeArray,'No',conmat(i,2));
            for j=1:3
                Nod.U(j)=conmat(i,j+2);
                if strcmp(eletype,'Beam3d')
                    Nod.A(j)=conmat(i,j+5);
                end
            end
        case 3
            if strcmp(eletype,'Beam3d')
                Nod=findobj(ElementArray,'No',conmat(i,2));
                for j=1:3
                    if isnan(Nod.LN(1).F(j))
                        Nod.LN(1).F(j)=0;
                    end
                    if isnan(Nod.LN(2).F(j))
                        Nod.LN(2).F(j)=0;
                    end
                    if isnan(Nod.LN(1).M(j))
                        Nod.LN(1).M(j)=0;
                    end
                    if isnan(Nod.LN(2).M(j))
                        Nod.LN(2).M(j)=0;
                    end
                    Nod.LN(1).F(j)=Nod.LN(1).F(j)+(Nod.length*((7*conmat(i,j+2))+(3*conmat(i,j+5)))/20);
                    Nod.LN(2).F(j)=Nod.LN(2).F(j)+(Nod.length*((3*conmat(i,j+2))+(7*conmat(i,j+5)))/20);
                    Nod.LN(1).M(j)=Nod.LN(1).M(j)+(Nod.length^2*((3*conmat(i,j+2))+(2*conmat(i,j+5)))/60);
                    Nod.LN(2).M(j)=Nod.LN(2).M(j)+(-Nod.length^2*((2*conmat(i,j+2))+(3*conmat(i,j+5)))/60);
                end
            end
    end
end
end

