-- at first, our jpg files' dir name is hard to use under shell environment
-- they looks like : 'SonTi (1).jog.dir'
-- while calling shell command, we must use '\' befor [ ()]. it's annoying
-- we need to convert is into 'SonTi1.jpg.dir'
-- this scripts take  two filename list file, one is old, one is new
-- 'mv [old] [new]' command will be invoked by the order they appeared in those two file
-- Must make sure that:  the order of filelists in old ~ new are matched!!
-- use extra '| sort' command before you create the old and new file is recommended

require 'torch'
cmd = torch.CmdLine();
cmd:option('-old', "old");
cmd:option('-new', "new");
opt = cmd:parse(arg or {});

oldDir = io.open(opt.old);
newDir = io.open(opt.new);

while true do
    oldline = oldDir:read();
    newline = newDir:read();
    if oldline == nil then break end
    os.execute("mv " .. oldline .. ' ' .. newline)
end
    

oldDir:close();
newDir:close();
