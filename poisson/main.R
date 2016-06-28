# set a working directory where all data files are placed
setwd("~/Desktop/Peacock/")

# import the rjags package
suppressPackageStartupMessages(library(rjags))
load.module('glm')

for (expr in c('Frontal', 'Back', 'Female')){
  for (directed in c('Both', 'Directed', 'NonDirected')){
    for (eye in c('Both', 'L', 'R')){
      # there are cases with zero counts, we don't run on them
      if (!(paste(expr, directed, eye, sep = ' ') %in% c('Back NonDirected Both', 'Back NonDirected R', 'Female NonDirected Both', 'Female NonDirected R', 'Female NonDirected L'))) {
        print(paste(expr, directed, eye, sep = ' '))
        modstr = 'poisson'
        bugstr=paste(modstr,".bug",sep="")
        datstr=paste('data/input/',expr,'_',directed,'_',eye,'.R',sep='')
        maxcount=10000
        
        # 3) Read in data and initialize JAGS model:
        d <- read.jagsdata(datstr)
        m <- jags.model(bugstr, d, n.chains=5,n.adapt=1000)
        
        # 4) Update the chain (burn-in):
        update(m,5000)
        
        qnames = c(d$roinames,'Mean',c('female std','male std','disp std'))
        x <- coda.samples(m, c('beta','mstd','fstd','odstd','B','N','M'), n.iter=20000,thin=100)
        
        # 6) Now, do diagnostics:
        jagssum=summary(x)
        ss<-jagssum$statistics
        qq<-jagssum$quantiles
        rejectionRate(x)
        ff=effectiveSize(x)
        xx = do.call(rbind,x)
        
        # 7) Grab quantiles for most the important variables:
        sel=grepl('B',rownames(qq))|grepl('M',rownames(qq))|grepl('E',rownames(qq))|grepl('lp',rownames(qq))|grepl('std',rownames(qq))
        post.quants=qq[sel,] #posterior quantiles
        rownames(post.quants) <- qnames #label correctly
        write.table(post.quants,file=paste('data/output/',expr,'_',directed,'_',eye,'.csv', sep=''),row.names=TRUE,col.names=NA,sep=',')
      }
    }
  }
}