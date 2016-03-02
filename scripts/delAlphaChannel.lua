-- typically, screenshots saved under Windows OS contain four channels, RGBa
-- this script will delete the fourth channel or the alpha channel

require 'image'
require 'torch'
cmd = torch.CmdLine();
cmd:option('-fname', 'nil', 'input filename')
opt = cmd:parse(arg or {});

pic = image.load(opt.fname);
image.save(opt.fname, pic[{{1,3},{},{}}])
