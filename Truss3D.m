    clear;
ElementType='Truss';
InputFilename='Input file';
NodeInput=xlsread(InputFilename,'Truss3D','A:J');
ElementInput=xlsread(InputFilename,'Truss3D','L:P');
NodeArray=NodalPoint(NodeInput,ElementType);
ElementArray=TrussElement(NodeArray,ElementInput);
K=GlobalStiffnessAssembler(NodeArray,ElementArray);
Stiffness=K;
numU=[NodeArray.U]';
numF=[NodeArray.F]';
% numU=numU(:);
% numF=numF(:);
zeropos=find(numU==0);
valpos=find(numU);
nanpos=find(isnan(numU));
valpos=setdiff(valpos,nanpos);
for i=nanpos
    if numF(i)==0
        numF(i)=0;
    end
end
if isempty(valpos)
    numU(nanpos)=LUSolverPP(K(nanpos,nanpos),numF(nanpos));
else
    numU(nanpos)=LUSolverPP(K(nanpos,nanpos),numF(nanpos)-(K(nanpos,valpos)*numU(valpos)));
end
disp(numU);
numF([zeropos valpos])=K([zeropos valpos],[nanpos valpos])*numU([nanpos valpos]);
disp(numF);
for i=1:size(NodeArray,2)
    NodeArray(i).U=numU((3*i)-2:3*i)';
    NodeArray(i).F=numF((3*i)-2:3*i)';
end
