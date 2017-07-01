clear;
InputFilename='DataFile.xlsx';
[~,ElementType]=xlsread(InputFilename,'Input','A1:A1');
[~,Solver]=xlsread(InputFilename,'Input','A5:A5');
NodeInput=xlsread(InputFilename,'Input','C:F');
ElementInput=xlsread(InputFilename,'Input','H:K');
MaterialInput=xlsread(InputFilename,'Input','V:AE');
ConstraintInput=xlsread(InputFilename,'Input','M:T');
NodeArray=NodalPoint(NodeInput);
if strcmp(ElementType,'Beam3D')
    %ElementArray=Beam3DElement(NodeArray,ElementInput,MaterialInput);
    error('Beam3D element is not ready. Only Trusses are available.');
else
    ElementArray=TrussElement(NodeArray,ElementInput,MaterialInput);
end
ApplyConstraints(NodeArray,ConstraintInput,ElementArray);
K=GlobalStiffnessAssembler(NodeArray,ElementArray);
Stiffness=K;

if isa(ElementArray,'Beam3DElement')
    eletype=6;
else
    eletype=3;
end
numU=zeros(size(NodeArray,2)*eletype,1)*nan;
numF=zeros(size(NodeArray,2)*eletype,1)*nan;
for i=1:size(NodeArray,2)
    for j=1:3
        numU((eletype*i)+j-eletype)=NodeArray(i).U(j);
        numF((eletype*i)+j-eletype)=NodeArray(i).F(j);
        if strcmp(ElementType,'Beam3D')
            numU((eletype*i)+3+j-eletype)=NodeArray(i).A(j);
            numF((eletype*i)+3+j-eletype)=NodeArray(i).M(j);
        end
    end
end

zeropos=find(numU==0);
valpos=find(numU);
nanpos=find(isnan(numU));
valpos=setdiff(valpos,nanpos);
for i=nanpos'
    if isnan(numF(i))
        numF(i)=0;
    end
end
if isempty(valpos)
    if strcmp(Solver,'LUP')
        numU(nanpos)=LUSolverPP(K(nanpos,nanpos),numF(nanpos));
    else
        numU(nanpos)=LUSolverCP(K(nanpos,nanpos),numF(nanpos));
    end
else
    if strcmp(Solver,'LUP')
        numU(nanpos)=LUSolverPP(K(nanpos,nanpos),numF(nanpos)-(K(nanpos,valpos)*numU(valpos)));
    else
        numU(nanpos)=LUSolverCP(K(nanpos,nanpos),numF(nanpos)-(K(nanpos,valpos)*numU(valpos)));
    end
end
numF([zeropos valpos])=K([zeropos valpos],[nanpos valpos])*numU([nanpos valpos]);

for i=1:size(NodeArray,2)
    for j=1:3
        NodeArray(i).U(j)=numU((eletype*i)+j-eletype);
        NodeArray(i).F(j)=numF((eletype*i)+j-eletype);
    end
end
for i=1:size(ElementArray,2)
    ElementArray(i).calcResults();
end
NodeOut=zeros(size(NodeArray,2),7);
ElemOut=zeros(size(ElementArray,2),4);
for i=1:size(NodeArray,2)
    NodeOut(i,1)=NodeArray(i).No;
    NodeOut(i,2)=NodeArray(i).U(1);
    NodeOut(i,3)=NodeArray(i).U(2);
    NodeOut(i,4)=NodeArray(i).U(3);
    NodeOut(i,5)=NodeArray(i).F(1);
    NodeOut(i,6)=NodeArray(i).F(2);
    NodeOut(i,7)=NodeArray(i).F(3);
end
for i=1:size(ElementArray,2)
    ElemOut(i,1)=ElementArray(i).No;
    ElemOut(i,2)=ElementArray(i).Force;
    ElemOut(i,3)=ElementArray(i).Stress;
    ElemOut(i,4)=ElementArray(i).Strain;
end
xlswrite(InputFilename, NodeOut,'Output',strcat('A2:G',num2str(size(NodeOut,1)+1)));
xlswrite(InputFilename, ElemOut,'Output',strcat('I2:L',num2str(size(ElemOut,1)+1)));

fig=figure;
for i=1:size(ElementArray,2)
    plot3([ElementArray(i).LN(1).X ElementArray(i).LN(2).X],[ElementArray(i).LN(1).Y ElementArray(i).LN(2).Y],[ElementArray(i).LN(1).Z ElementArray(i).LN(2).Z],'b')
    hold on;
end
for i=1:size(ElementArray,2)
    plot3([ElementArray(i).LN(1).X+ElementArray(i).LN(1).U(1) ElementArray(i).LN(2).X]++ElementArray(i).LN(2).U(1),[ElementArray(i).LN(1).Y+ElementArray(i).LN(1).U(2) ElementArray(i).LN(2).Y+ElementArray(i).LN(2).U(2)],[ElementArray(i).LN(1).Z+ElementArray(i).LN(1).U(3) ElementArray(i).LN(2).Z+ElementArray(i).LN(2).U(3)],'r');
    hold on;
end
hold off;
print(fig,'DeformedTruss','-djpeg');
