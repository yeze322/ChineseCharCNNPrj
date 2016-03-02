-- typically, t7 datafile created by pakageData.lua don't contain tag
-- this script is used to add data lable for the trainset
-- read each 'dataset.t7' file under all kinds of fonts' root dir
-- then convert unlabeled data to labeled data called 'labeldata.t7'
-- the label index order will follow the fonts' dir's appearence order in 'find ./ -name "*dataset.t7"' command
-- a diction for 'Chinese fonts name' ~ 'numeric index' will be created and saved to the path under which this scripts is executed

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

searchRootPath = './'
print('search path = ' .. searchRootPath)
query = io.popen('find ' .. searchRootPath .. ' -name "*dataset.t7"')

index = 0
index_dic = {}
while true do
    index = index + 1
    line = query:read()
    if line == nil then break end
    print('modifing: ' .. line)
    -- split the path
    pref, dir, fname = line:match'(.*)/(.*)/(.*)'
    -- map 'Chinese Font Name' - 'numberic index'
    index_dic[dir] = index;
    -- add numeric tags
    local saveset = {}
    saveset.dataset = torch.load(line);
    saveset.label = torch.Tensor(saveset.dataset:size(1)):fill(index);
    newfname = pref .. '/' .. dir .. '/' .. 'labeldata.t7'
    print('saving:' .. newfname)
    torch.save(newfname, saveset);
    saveset = nil;
    collectgarbage();
end 

torch.save('index_dic.t7', index_dic)
