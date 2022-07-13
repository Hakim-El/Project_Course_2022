%%
clear
close all
clc
%%

trueSpkrPos=[
    1.44, 3.39, 1.16;
    2.17, 3.40, 1.15;
    1.42, 2.67, 1.15;
    2.19, 2.645, 1.16;
    1.39, 1.92, 1.16;
    2.20, 1.835, 1.15;
];

micPos1 = [ 0.49407,  4.4825, 0.52685;
    1.1858,  4.3940, 0.39627;
    1.75844,  4.3953, 0.453863;
    2.3082, 4.44356, 0.404805;
    3.01739, 4.49936, 0.55059;
    0.62896,  3.8204, 1.13962;
    1.17475,  3.7361, 1.14012;
    1.7829, 3.79040, 1.14402;
    2.3930, 3.78959, 1.14212;
    3.06083,  3.8364, 1.10570;
    0.64311,  3.2220, 2.04734;
    1.12475, 3.25235, 2.04733;
    1.89890, 3.24850, 2.03256;
    2.47427, 3.21023, 2.03573;
    3.03768, 3.29436, 2.0355];

spkrPos1 = [
    1.4087            3.303            1.1822;
    2.1373            3.333            1.1700;
    1.4375            2.651            1.1941;
    2.122            2.6551            1.1905;
    1.377            1.9405            1.2247;
    2.178            1.8690            1.2092;];

micPos2 = [            0.53808, 3.90080, 0.46408;
    1.1024, 3.8870, 0.46095;
    1.78904, 3.84936 0.47954;
    2.3473, 3.8109, 0.4826;
    2.9455, 3.8394, 0.4781;
    0.6018, 3.2449, 1.1484;
    1.0400, 3.2391, 1.1533;
    1.8070, 3.2219, 1.1472;
    2.460, 3.216, 1.1111;
    2.9219, 3.2310, 1.1214;
    0.6341, 2.7123, 2.0466;
    1.0035, 2.7083, 2.0639;
    1.816, 2.690, 2.045;
    2.4279, 2.7032, 2.0546;
    2.9238, 2.6978, 2.0451;];

spkrPos2 = [           1.40790,            3.40877,            1.22031;
    2.14266            3.446473            1.22501;
    1.43166            2.63082,            1.1792;
    2.11783            2.64400,            1.18087;
    1.36974,            1.93907,            1.22065;
    2.18015            1.869958,            1.20988;];





micPos3 = [
    0.60362,  3.28614, 0.5136;
    1.1283  3.2677,  0.4671;
    1.7309, 3.27990, 0.49720;
    2.251 3.283 0.49474;
    2.876 3.28413, 0.48966;
    0.60263,  2.79977, 1.1373;
    1.12687,  2.75427, 1.1867;
    1.71392,  2.70933, 1.1519;
    2.4232,   2.67054,  1.145;
    2.88394,  2.65526, 1.1146;
    0.61864,  2.16157, 2.0525;
    1.1164  2.14653,  2.0675;
    1.77227,  2.1284, 2.0706;
    2.33537,   2.14834,  2.057;
    2.87956,   2.1433,  2.043;];
spkrPos3= [
    1.433714,            3.3786806,            1.1436;
    2.1591,            3.431199,            1.1693;
    1.457708,            2.517026,            1.0808;
    2.12628,            2.874128,            1.315;
    1.38548,            1.9637906,            1.2165;
    2.188854,            1.8856006,            1.2107;];



micPos4= [
    0.6607,            2.6079,            0.5079;
    1.0685,            2.6087,            0.5163;
    1.707,            2.610,            0.508;
    2.20784,            2.62148,            0.52181;
    2.864359,            2.648085,            0.496601;
    0.61513,            2.08594,            1.16058;
    1.1141,            2.0734,            1.1582;
    1.68262,            2.08170,            1.15702;
    2.19720,            2.09114,            1.16980;
    2.87484,            2.05845,            1.12794;
    0.6144,            1.5092,            2.0652;
    1.1538,            1.5207,            2.0673;
    1.6803,            1.5048,            2.0792;
    2.20364,            1.50252,            2.06355;
    2.883,            1.503,            2.056;];

spkrPos4 = [1.435,           3.391,            1.157;
    2.1598            3.4405,            1.1761;
    1.4626            2.7344,            1.2351;
    2.1200            2.7247,            1.2049;
    1.3782            2.1236,            1.2970;
    2.2009            1.9026,            1.2064;];

micPos5 = [            0.4642,            2.0900,            0.5057;
    1.0366,            2.1018,            0.5145;
    1.6505,            2.0819,            0.5121;
    2.1688,            2.0791,            0.5414;
    2.9469,            2.0243,            0.4957;
    0.4679,            1.4102,            1.1413;
    1.0845,            1.4999,            1.1700;
    1.6479,            1.4618,            1.1501;
    2.2203,            1.4550,            1.1300;
    2.9560,            1.4469,            1.1298;
    0.5031,            0.8702,            2.0746;
    1.0602,            0.9237,            2.0791;
    1.6597,            0.8822,            2.0739;
    2.199,            0.892,            2.069;
    2.972,            0.877,            2.062;];
spkrPos5 = [            1.3985,            3.3891,            1.1772;
            2.1218,            3.4445,            1.1751;
            1.4210,            2.7058,            1.2195;
            2.1028,            2.7062,            1.1745;
            1.3545,            2.0120,            1.1828;
            2.1773,            1.9679,            1.2074;];

micPos6 = [
            0.3342,            1.3375,            0.4856;
            0.939,            1.425,            0.506;
            1.626,            1.449,            0.533;
            2.189,            1.461,            0.556;
            3.009,            1.458,            0.531;
            0.398,            0.795,            1.131;
            0.961,            0.822,            1.159;
            1.644,            0.872,            1.172;
            2.209,            0.862,            1.148;
            3.057,            0.855,            1.164;
            0.413,            4.409,            2.057;
            1.045,            4.416,            2.004;
            1.726,            4.451,            2.029;
            2.195,            4.458,            2.008;
            2.96,            4.47,            2.03;];
        
spkrPos6 = [            1.334,            3.358,            1.196;
            2.047,            3.433,            1.121;
            1.356,            2.675,            1.208;
            2.024,            2.708,            1.131;
            1.297,            2.012,            1.128;
            2.116,            1.945,            1.207;];
        
micPos7 = [
            0.605,            0.541,            0.567;
            1.17,            0.64,            0.63;
            1.641,            0.703,            0.687;
            2.180,            0.686,            0.641;
            2.750,            0.728,            0.635;
            0.528,            4.212,            1.142;
            1.103,            4.233,            1.139;
            1.739,            4.250,            1.154;
            2.224,            4.267,            1.159;
            2.96,            4.29,            1.11;
            0.58,            3.62,            2.03;
            1.110,            3.600,            2.011;
            1.680,            3.650,            2.006;
            2.23,            3.65,            2.00;
            2.941,            3.700,            2.007;];
        
        
micPos7_2 = [
        0.49066,0.57064,0.50297;
        1.04640,0.68864,0.54425;
        1.68740,0.76270,0.59091;
        2.17383,0.83174,0.58020;
        2.96766,0.89573,0.58474;
        0.46228,4.46261,1.10371;
        1.05152,4.44659,1.13106;
        1.65806,4.44854,1.14832;
        2.17103,4.47070,1.13855;
        2.93780,4.45189,1.08794;
        0.50032,3.72504,2.05421;
        1.04932,3.71810,2.03247;
        1.63622,3.77888,2.01767;
        2.21695,3.78938,2.02097;
        2.93757,3.83328,2.02541;
        ];
    
spkrPos7 =[
           1.4064,            3.1801,            1.2490;
            2.139,            3.222,            1.231;
           1.4216,            2.5409,            1.2088;
            2.103,            2.522,            1.218;
           1.3342,            1.8437,            1.2206;
            2.1718,            1.7561,            1.3066;];       
        
spkrPos7_2 =[
            1.3628672081806155,3.2584313236327827,1.2491714376434102;
            2.0955113405765893,3.3290464853033597,1.2117820765798315;
            1.382746571965173,2.6205737526934825,1.2045571569825366;
            2.0581561942867115,2.6116861071923836,1.214853137283191;
            1.3140704194281796,1.9168616805861323,1.2201176788363295;
            2.1260914933911645,1.833971273505931,1.3012399196184987;];

LSArrayPos = [
          1.55, 0, 1.67;
          1.625, 0, 1.445;
          1.7, 0, 1.67;
          1.775, 0, 1.445;
          1.85, 0, 1.67;
          1.925, 0, 1.445;
          2, 0, 1.67;
          2.075, 0, 1.445];
        
% mic1Mean = mean([micPos1(1,:) ;micPos2(1,:) ;micPos3(1,:) ;micPos4(1,:) ;
%     micPos5(1,:) ;micPos6(1,:) ;micPos7(1,:) ;]);
% mic2Mean = mean([micPos1(2,:) ;micPos2(2,:) ;micPos3(2,:) ;micPos4(2,:) ;
%     micPos5(2,:) ;micPos6(2,:) ;micPos7(2,:) ;]);
% mic3Mean = mean([micPos1(3,:) ;micPos2(3,:) ;micPos3(3,:) ;micPos4(3,:) ;
%     micPos5(3,:) ;micPos6(3,:) ;micPos7(3,:) ;]);
% mic4Mean = mean([micPos1(4,:) ;micPos2(4,:) ;micPos3(4,:) ;micPos4(4,:) ;
%     micPos5(4,:) ;micPos6(4,:) ;micPos7(4,:) ;]);
% mic5Mean = mean([micPos1(5,:) ;micPos2(5,:) ;micPos3(5,:) ;micPos4(5,:) ;
%     micPos5(5,:) ;micPos6(5,:) ;micPos7(5,:) ;]);
% mic6Mean = mean([micPos1(6,:) ;micPos2(6,:) ;micPos3(6,:) ;micPos4(6,:) ;
%     micPos5(6,:) ;micPos6(6,:) ;micPos7(6,:) ;]);
% mic7Mean = mean([micPos1(7,:) ;micPos2(7,:) ;micPos3(7,:) ;micPos4(7,:) ;
%     micPos5(7,:) ;micPos6(7,:) ;micPos7(7,:) ;]);
% mic8Mean = mean([micPos1(8,:) ;micPos2(8,:) ;micPos3(8,:) ;micPos4(8,:) ;
%     micPos5(8,:) ;micPos6(8,:) ;micPos7(8,:) ;]);
% mic9Mean = mean([micPos1(9,:) ;micPos2(9,:) ;micPos3(9,:) ;micPos4(9,:) ;
%     micPos5(9,:) ;micPos6(9,:) ;micPos7(9,:) ;]);
% mic10Mean = mean([micPos1(10,:) ;micPos2(10,:) ;micPos3(10,:) ;micPos4(10,:) ;
%     micPos5(10,:) ;micPos6(10,:) ;micPos7(10,:) ;]);
% mic11Mean = mean([micPos1(11,:) ;micPos2(11,:) ;micPos3(11,:) ;micPos4(11,:) ;
%     micPos5(11,:) ;micPos6(11,:) ;micPos7(11,:) ;]);
% mic12Mean = mean([micPos1(12,:) ;micPos2(12,:) ;micPos3(12,:) ;micPos4(12,:) ;
%     micPos5(12,:) ;micPos6(12,:) ;micPos7(12,:) ;]);
% mic13Mean = mean([micPos1(13,:) ;micPos2(13,:) ;micPos3(13,:) ;micPos4(13,:) ;
%     micPos5(13,:) ;micPos6(13,:) ;micPos7(13,:) ;]);
% mic14Mean = mean([micPos1(14,:) ;micPos2(14,:) ;micPos3(14,:) ;micPos4(14,:) ;
%     micPos5(14,:) ;micPos6(14,:) ;micPos7(14,:) ;]);
% mic15Mean = mean([micPos1(15,:) ;micPos2(15,:) ;micPos3(15,:) ;micPos4(15,:) ;
%     micPos5(15,:) ;micPos6(15,:) ;micPos7(15,:) ;]);
% 
% micMean = [mic1Mean;mic2Mean;mic3Mean;mic4Mean;mic5Mean;mic6Mean;mic7Mean;
%     mic8Mean;mic1Mean;mic1Mean;mic1Mean;mic1Mean;mic1Mean;mic1Mean;mic1Mean;];


sourceMean = spkrPos1;
sourceMean(:,:,2) = spkrPos2;
sourceMean(:,:,3) = spkrPos3;
sourceMean(:,:,4) = spkrPos4;
sourceMean(:,:,5) = spkrPos5;
sourceMean(:,:,6) = spkrPos6;
sourceMean(:,:,7) = spkrPos7_2;
sourceMean = mean(sourceMean,3);
%% Source positions
figure
scatter3(spkrPos1(:,1), spkrPos1(:,2), spkrPos1(:,3),'*'), hold on;
scatter3(spkrPos2(:,1), spkrPos2(:,2), spkrPos2(:,3),'*');
scatter3(spkrPos3(:,1), spkrPos3(:,2), spkrPos3(:,3),'*');
scatter3(spkrPos4(:,1), spkrPos4(:,2), spkrPos4(:,3),'*');
scatter3(spkrPos5(:,1), spkrPos5(:,2), spkrPos5(:,3),'*');
scatter3(spkrPos6(:,1), spkrPos6(:,2), spkrPos6(:,3),'*');
scatter3(spkrPos7_2(:,1), spkrPos7_2(:,2), spkrPos7_2(:,3),'*');
scatter3(trueSpkrPos(:,1), trueSpkrPos(:,2), trueSpkrPos(:,3),  'filled', 'black', 'diamond');


xlim([0, 3.64]), ylim([0, 5]), zlim([0, 2.5]);
title('Source Position')

figure
scatter3(sourceMean(:,1), sourceMean(:,2), sourceMean(:,3),'*'), hold on;
scatter3(trueSpkrPos(:,1), trueSpkrPos(:,2), trueSpkrPos(:,3),  'filled', 'black', 'diamond');

xlim([0, 3.64]), ylim([0, 5]), zlim([0, 2.5]);
title('Mean Source Position')
%% Mic Positions

figure
scatter3(micPos1(:,1), micPos1(:,2), micPos1(:,3), 'filled'), hold on;
scatter3(micPos2(:,1), micPos2(:,2), micPos2(:,3), 'filled');
scatter3(micPos3(:,1), micPos3(:,2), micPos3(:,3), 'filled');
scatter3(micPos4(:,1), micPos4(:,2), micPos4(:,3), 'filled');
scatter3(micPos5(:,1), micPos5(:,2), micPos5(:,3), 'filled');
scatter3(micPos6(:,1), micPos6(:,2), micPos6(:,3), 'filled');
scatter3(micPos7_2(:,1), micPos7_2(:,2), micPos7_2(:,3), 'filled');

xlim([0, 3.64]), ylim([0, 5]), zlim([0, 2.5]);
title('Mic Position')
%% Source And Mic Positions
figure
scatter3(micPos2(:,1), micPos2(:,2), micPos2(:,3),'x','MarkerEdgeColor', '#D95319'), hold on;
scatter3(spkrPos2(:,1), spkrPos2(:,2), spkrPos2(:,3),'r','o','filled'), hold on;

xlim([0, 3.64]), ylim([0, 5]), zlim([0, 2.5]);
xlabel('x [m]','Fontsize',12)
ylabel('y [m]','Fontsize',12)
zlabel('z [m]','Fontsize',12)
legend('Estimated Microphone Position','Estimated Loudspeaker Position','FontSize',12)
title('Experimental results','Fontsize',16)

%% Statistics
xlim([0, 3.64]), ylim([0, 5]), zlim([0, 2.5]);
title('all')

figure, imagesc(pdist2(spkrPos2, spkrPos5))

figure, imagesc(pdist2([spkrPos1; spkrPos2; spkrPos3; spkrPos4; spkrPos5; spkrPos6; spkrPos7], ... 
    [spkrPos1; spkrPos2; spkrPos3; spkrPos4; spkrPos5; spkrPos6; spkrPos7]),[0.01, 0.5])
colorbar, colormap(flipud(colormap(('gray'))));

















