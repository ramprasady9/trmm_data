clear
clc

n=1000;
mu = [0 0];
sigma = [1 0; 0 1];

rng('default')  % For reproducibility
R = mvnrnd(mu,sigma,n);

tau=corr(R(:,1),R(:,2),'type','kendall');
rho=corr(R(:,1),R(:,2),'type','spearman');

%% Fitting Clayton and Gumbel Copula
% a=normcdf(R(:,1),0,1);
% b=normcdf(R(:,2),1.1,4);
a=rank(R(:,1))/(n+1);
b=rank(R(:,2))/(n+1);

% b=betacdf(R(:,2),2,2);
% b(b==0)=0.0001;
% b(b==1)=1-0.0001;
% scatter(a,b,10,c,'fill');

%% for plotting
x=linspace(0,1,n);
[u1,u2] = meshgrid(x,x);

u1_inv=norminv(u1,0,1);
u2_inv=norminv(u2,0,1);
% u2_inv=betainv(u2,2,2);
y=mvncdf([u1_inv(:),u2_inv(:)],mu,sigma);
y_mat=reshape(y,n,n);
contour(u1_inv,u2_inv,y_mat);
axis equal;
hold on;

yc=copulacdf('Gaussian',[u1(:),u2(:)],sigma)';
yc_mat=reshape(yc,n,n);
contour(u1_inv,u2_inv,yc_mat,'LineStyle','--','LineWidth',2);
legend({'MVNCDF','COPULA'});
% s.EdgeColor='none';
xlabel('u');
ylabel('v');
colorbar

clearvars yc y;
