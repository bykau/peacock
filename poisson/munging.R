library(reshape)


setwd('~/Dropbox/Projects/Jessica/peacock/poisson/')
for (expr in c('Frontal', 'Back', 'Female')){
  for (directed in c('Both', 'Directed', 'NonDirected')){
    for (eye in c('Both', 'L', 'R')){
      dat <- read.csv(paste('data/',expr,'.csv',sep = ''), colClasses = c('factor', rep('numeric', 8), rep('factor', 3), rep('numeric', 6), rep('factor', 2)))
      dat$ntot <- dat[,paste('Total',expr,'ImageFrames', sep = '')] + dat$TotalEnvirFrames
      if (directed != 'Both') {
        dat <- dat[dat$ClipType == directed, ]
      }
      if (eye != 'Both') {
        dat <- dat[dat$EyeRecord == eye, ]
      }
      # we have zero counts for BlackFluff ROI so we remove it
      dat <- dat[dat$ROI != 'BlackFluff',]

      # group by MaleID, ROI and OtherMaleID and summing total frames/counts
      count_df <- as.data.frame(recast(dat[, c('ntot', 'MaleID', 'ROI', 'Count', 'OtherMaleID')], MaleID + ROI + OtherMaleID ~ variable, fun.aggregate = sum))
      
      # pixel sizes are averaged across all clips (again, grouped by MaleID, ROI and OtherMaleID)
      pix_df <- as.data.frame(recast(dat[, c('MaleID', 'ROI', 'PixelSize', 'OtherMaleID')], MaleID + ROI + OtherMaleID ~ variable, fun.aggregate = mean))
      
      # join count_df and pix_df by MaleID, ROI and OtherMaleID
      count_df <- merge(count_df, pix_df)
      
      # the same size of TotalPixels
      pixnorm = 1454590
      
      # dumping data into Prof. Pearson's format
      count <- count_df$Count
      ntot <- count_df$ntot
      pix = count_df$PixelSize/pixnorm
      roi = as.integer(count_df$ROI)
      # the role of male plays the other male who is being looked at
      male = as.integer(count_df$OtherMaleID)
      # the role of female plays a 'looking' male 
      fem = as.integer(count_df$MaleID)
      nmale = length(levels(count_df$OtherMaleID))
      nfem = length(levels(count_df$MaleID))
      nroi = length(levels(count_df$ROI))
      roinames = levels(count_df$ROI)
      dumplist = c('count','ntot','pix','roi','male','fem','nmale','nfem','nroi','roinames')
      dump(dumplist,file=paste('data/input/', expr, '_', directed, '_', eye, '.R', sep = ''))
    }
  }
}
