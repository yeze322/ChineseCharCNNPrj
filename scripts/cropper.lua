-- This script is used to split a full screen shot into several single character
-- Under my data source, we can got 1080 char per img
-- Use single shell command to change the output dir and format
-- use shell to call this script automatically

require 'image'
require 'torch'

cmd = torch.CmdLine();
cmd:option('-fname','sample.png','type the jpg file name here');
opt = cmd:parse(arg or {});

BEGIN = {ROW=57, COL=62};
END = {ROW=1028, COL=1741};

INTERVAL = {ROW=36, COL=42};
WINDOW = INTERVAL.ROW

pic = image.load(opt.fname);
dst = torch.Tensor(3, WINDOW, WINDOW);

N = 0
-- os.execute('mkdir ......') may be needed
for m=BEGIN.ROW, END.ROW-1, INTERVAL.ROW do
    for n=BEGIN.COL, END.COL-1, INTERVAL.COL do
        image.crop(dst, pic, n, m);
        -- itorch.image(dst);
        N = N + 1;
        image.save(opt.fname .. '.dir/' .. N .. '.jpg', dst);
    end
end

print(opt.fname .. '[Finished!]')
