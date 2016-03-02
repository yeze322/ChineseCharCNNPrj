--[[
This script is used to merge several pakages of different fonts together.
There is some conflict in how to set data label, but it's not very serious. just ignore it.
a file which contains the fonts name must be provided. the default fname is uselist.

this sctipt also shuffle the data, controled by the cmd option -shuffle = 'true' or else.
]]--
require 'torch'
require 'os'

-- command line args
cmd = torch.CmdLine();
cmd:option('-basedir','/home/yeze/Desktop/ChineseCharPrj/traindata/','path to search data and dic file');
cmd:option('-fin','uselist','which fonts to use? save in file')
cmd:option('-outputfname','trainset.t7', 'default output dataset file name')
cmd:option('-outputdir','./','output file name')

cmd:option('-datasuffix', '_tagged.t7','data file name suffix')
cmd:option('-shuffle','true','if shuffle the data?')

cmd:option('-beginindex',1,'data segment start point')
cmd:option('-length', -1,'data segment length')
opt = cmd:parse(arg or {})

-- read fonts list from local file
local fp = io.open(opt.basedir .. opt.fin);
if fp == nil then print('invalid uselise, please check') os.exit() end

local lb_font_dict = {} -- 1:songti
local font_lb_dict = {} -- songti:1

local flist = {}
local index = 0
while true do
    line = fp:read()
    if line == nil then break end
    index = index + 1
    lb_font_dict[index] = line
    font_lb_dict[line] = index
    local data = torch.load(opt.basedir .. line .. opt.datasuffix)
    flist[#flist+1] = data
end
io.close(fp)

-- data segment length modified
if opt.length == -1 then opt.length = flist[1].dataset:size(1) - opt.beginindex; end
local total_size = opt.length * #flist;
print('total size = ' .. total_size .. '(' .. opt.length .. '*' .. #flist .. ')');

-- get prigin data size e.g. n*3*36*36, then modify the first which indicates number
elementsize = flist[1].dataset:size();
elementsize[1] = total_size;

traindata = {}
traindata.data = torch.Tensor(elementsize):byte();
traindata.label = torch.Tensor(total_size):byte();

-- merge different fonts together
local accumulate = 0;
for i=1,#flist do
    -- save data
    traindata.data[{{accumulate+1,accumulate+opt.length},{},{},{}}] = flist[i].dataset[{{opt.beginindex, opt.beginindex+opt.length-1},{},{},{}}];
    -- save label
    -- traindata.label[{{accumulate+1, accumulate+size}}] = flist[i].label;
    traindata.label[{{accumulate+1, accumulate+opt.length}}]:fill(i);
    accumulate = accumulate + opt.length;
    print(lb_font_dict[i] .. ' added: ' .. opt.beginindex .. ' ~ ' .. opt.beginindex + opt.length - 1)
end
print(traindata);
print('Finish packaging!' .. accumulate .. '/' .. total_size)

if opt.shuffle == 'true' then
    -- shuffle data in a random order
    local shuffer = torch.randperm(total_size);
    local shufdata = torch.Tensor(traindata.data:size()):byte();
    local shuflabel = torch.Tensor(traindata.label:size()):byte();
    for i=1,total_size do
        shufdata[i] = traindata.data[shuffer[i]]
        shuflabel[i] = traindata.label[shuffer[i]]
    end
    
    traindata.data = shufdata;
    traindata.label = shuflabel;
    print('Finish shuffling the dataset!')
end


-- save diction, dataset
local saveName = {}
saveName.dictionname = 'diction.t7';
saveName.datasetname = opt.outputfname;
local diction = {}
diction.bylabel = lb_font_dict
diction.byfont = font_lb_dict
torch.save(opt.outputdir .. saveName.dictionname, diction)
print('diction saved at: ' .. opt.outputdir .. saveName.dictionname)

torch.save(opt.outputdir .. saveName.datasetname, traindata)
print('dataset saved at: ' .. opt.outputdir .. saveName.datasetname)

collectgarbage();
