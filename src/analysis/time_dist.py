#!/usr/bin/env python
import os
import sys
import csv
import pickle
from rep_db import *
from datetime import *

#from trend_plot import trendObj
from time_plot import timePlot
import time_plot

class trendObj:
    def __init__(self,metric,commit_meta=None):
        self.metric = metric
        if commit_meta is not None:
            print commit_meta
            self.commitId = commit_meta.commitId
            self.projId = commit_meta.projId
            self.date = commit_meta.date
            self.author = commit_meta.author

        self.fileDist = {}

    def __repr__(self):
        return "{0}:{1}".format(self.commitId,self.metric)


def showTimeDist(rep_db):

    cloneList = rep_db.clones
    commitId2Meta = rep_db.commits

    proj0_time = {} #map between commitId and trendObj
    proj1_time = {}

    #first create data points for all commit_dates
    """
    for commit_id,commit_meta in commitId2Meta.iteritems():
        commit_date = rep_db.getCommitDate(commit_id)
#        print commit_date
#        print commit_id
        if commit_date is None:
            continue
        proj_trend = proj1_trend

        if rep_db.getProjId(commit_id) == 'proj0':
            proj_trend = proj0_trend
        proj_trend[commit_date] = trendObj(0,commit_meta)
    """
    #populate data points with metric
    for clMeta in cloneList:
        print "================="
        print clMeta
        lhs_id = clMeta.lhsCommitId
        rhs_id = clMeta.rhsCommitId
        metric = int(clMeta.metric)

        lcommit_date = rep_db.getCommitDate(lhs_id)
        rcommit_date = rep_db.getCommitDate(rhs_id)
        print "%s,%s" % (lcommit_date,rcommit_date)

        time_delta = abs(lcommit_date - rcommit_date)
#        time_delta = (time_delta.days * 24 * 60 * 60) + time_delta.seconds
        time_delta = time_delta.days
        print time_delta

        commit_id = lhs_id
        commit_date = lcommit_date
        if (lcommit_date <= rcommit_date):
            #porting is done to rhs project
            print "l <= r"
            commit_id = rhs_id
            commit_date = rcommit_date

        proj_time = proj1_time
        if rep_db.getProjId(commit_id) == 'proj0':
            proj_time = proj0_time
        if proj_time.has_key(time_delta) == 0:
            proj_time[time_delta] = 0
        proj_time[time_delta] += metric

    print proj0_time
    print proj1_time


    time_plot.draw(timePlot(proj0_time,proj1_time))

#---------------testing-----------------#

if __name__ == "__main__":
    if (len(sys.argv) < 2):
         print "Usage: time_dist.py rep_db.pickle"
         print "rep_db.pickle is pickle dump of rep output"
         sys.exit(2)

    print "time_dist.py: repertoire database: " + sys.argv[1]

    rep_db = pickle.load(open(sys.argv[1],"rb"))

    fileDist = showTimeDist(rep_db)
