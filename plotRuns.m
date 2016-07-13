
outdir = '/Users/mobeets/code/NBAclr/data/output';
fnms = dir(fullfile(outdir, 'out_*.mat'));
Hs = cell(numel(fnms),1);
vs = nan(numel(fnms),1);
for ii = 1:numel(fnms)
    fnm = fullfile(outdir, fnms(ii).name);
    tm = strsplit(fnm, '_');
    vs(ii) = str2num(tm{2});
    M = load(fnm);
    Hs{ii} = M.H;
end

%%

[~,ix] = sort(vs);
plot.init;
for ii = 1:numel(ix)
%     subplot(1,numel(ix),ii); hold on;
    subplot(2,3,ii); hold on;
    H = Hs{ix(ii)};
    imagesc(H);
    title(['Last ' num2str(vs(ix(ii))) ' minutes']);
    set(gca, 'XTick', 0:5:size(H,1)-1);
    set(gca, 'YTick', 0:5:size(H,2)-1);
    axis equal;
    if ii == numel(ix)
        xlabel('Team 1 score');
        ylabel('Team 2 score');
    end
end

%%

[~,ix] = sort(vs);
for ii = 1:numel(ix)
    H = Hs{ix(ii)};
    v = vs(ix(ii));
    [~,ind] = max(H(:));
    [xx,yy] = ind2sub(size(H), ind);
    [v xx yy]
end

%%

outdir = '/Users/mobeets/code/NBAclr/data/output';
M = load(fullfile(outdir, 'ptdiffs.mat'));
M = double(M.diffs);
hist(M, min(M):max(M))
