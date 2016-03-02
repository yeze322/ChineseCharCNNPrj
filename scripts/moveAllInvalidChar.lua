-- this scripts is used to scan whole jpg dir, and move those invalid single cha pics to ./invalid/
-- the rule for moving is simple, we check the file list under HuPo/index/invalid dir, 
-- and then move those files with the same name as HuPo fonts
-- neew to be executed under 'scripts/../'

require 'xlua'

function getcmdlines(command)
    local window = io.popen(command);
    local ret = {}
    local index = 0
    while true do
        local line = window:read();
        if line == nil then break end
        index = index + 1;
        ret[index] = line
    end
    return ret
end

cmd_hupo = 'find . -type d -mindepth 4 | grep hupo | sort'
hupo_invalid_dir_list = getcmdlines(cmd_hupo)

template = 'find . -type d -mindepth 3 -maxdepth 3 | grep -v hupo | grep '
-- dirs without hupo
dir_group = {}
for i=1,7 do dir_group[i] = getcmdlines(template .. i) end


-- start ls
for i=1,7 do
    print('\t\t[movind index] = ' .. i)
    local invalid_flist = getcmdlines('ls ' .. hupo_invalid_dir_list[i]);
    local rootDirs = dir_group[i];
    for a=1,#rootDirs do
        local originPath = rootDirs[a] .. '/';
        local newPath = originPath .. 'invalid/';
        print('moving path = ' .. originPath);
        for b=1,#invalid_flist do
            xlua.progress(b, #invalid_flist);
            os.execute('mv ' .. originPath .. invalid_flist[b] .. ' ' .. newPath);
        end
    end
end
