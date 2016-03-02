-- this script is used to pakage JPG data
-- will create a .t7 file under the fonts' root path
-- the data is a torch.Tensor type
-- cmd line parameters needed, esecially -dir
-- you can use is like : 'th [this script] -dir ./SongTi '

require 'torch'
require 'image'
cmd = torch.CmdLine();
cmd:option('-fname', 'JPG_list.txt', 'input jpg name set');
cmd:option('-oname', 'dataset.t7','output data set file name');
cmd:option('-dir','./','output dataset dir')
opt = cmd:parse(arg or {})

fp = io.open(opt.dir .. '/' .. opt.fname);
flist = {}
index = 0;
while true do
    index = index + 1
    local line = fp:read()
    if line == nil then break end
    flist[index] = line
end

dataset = torch.Tensor(#flist, 3, 36, 36):byte();

for i=1,#flist do
    dataset[i] = image.load(flist[i]):mul(255):byte();
end

torch.save(opt.dir .. '/' .. opt.oname, dataset)
print('pakage finished! dir = ' .. opt.dir)
