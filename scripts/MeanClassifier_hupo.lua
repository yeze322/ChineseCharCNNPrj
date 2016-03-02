-- this script is used to distinguish existed HuPo fonts and invalid fonts
-- those invalid, non HuPo single char will be move into an extra dir called './inalid'
require 'image'
require 'torch'

THRESOLD = 0.17

cmd = torch.CmdLine();
cmd:option('-fname', 'nil', 'calculate this file');
opt = cmd:parse(arg or {});

pic = image.load(opt.fname);
avg = pic:mul(-1):add(1):mean();

if avg<THRESOLD then
    dir, file = opt.fname:match("(.*)/(.*)");
    dir = dir:gsub(" ", "\\ ");
    dir = dir:gsub("[(]", "\\("):gsub("[)]", "\\)");
    execmd = 'mv ' .. dir .. '/' ..  file  .. " " .. dir .. "/invalid/"
    print(execmd)
    os.execute(execmd)
end
