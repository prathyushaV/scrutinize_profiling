import cProfile
import logging
import time


#### Added prathyusha
import pstats
import StringIO
import os

LOG = logging.getLogger(__name__)

path = os.path.split(os.getcwd())[0]

class Collector(object):
    def __init__(self, configuration):
        self.configuration = configuration
        LOG.debug("%s: Config=%s" % (self.__class__.__name__, configuration))

    def start(self, label):
        # NOTE: Don't store any state in this collector.
        # It will be reused many times. Return a state object
        # here and it will be given back to you in stop()
        return label

    def stop(self, state):
        return []

    def call_target(self, __state, __bundle, *args, **kwargs):
        return __bundle.target_impl(*args, **kwargs)


class Profile(Collector):

    def start(self, label):
        return dict(label=label)

    def stop(self, state):
        metrics = state['metrics']
        label = state['label']
        final = []
        #for total, callcount, this_label in metrics:
        #    final.append(("%s.%s" % (label, this_label), total))
        return final

    def _scrub(self, value):
        value = value.replace(".", "_")
        value = value.replace("/", "_")
        value = value.replace("|", "_")
        return value.replace(":", "_")

    def _label(self, code):
        if isinstance(code, str):
            return None    # built-in function
        filename = self._scrub(code.co_filename)
        name = self._scrub(code.co_name)
        return "%s.%s.line_%04d" % (filename, name, code.co_firstlineno)

    def call_target(self, __state, __bundle, *args, **kwargs):
        p = cProfile.Profile()
        #result = p.runcall(__bundle.target_impl, *args, **kwargs)
        #added Prathyusha
        label = __state['label']
        import datetime
        time_now = str(datetime.datetime.now()).split()[-1]
        result = p.runcall(__bundle.target_impl, *args, **kwargs)
        #if 'create' in label:
            #label = label + '_' +eval(args[1].body)['server']['name']
        #    label = label
        if not os.path.exists(path+'/scrutinize/stats-dump'):
            os.makedirs(path+'/scrutinize/stats-dump')
        p.dump_stats('%s/%s#%s.prof'%(path+\
                         '/scrutinize/stats-dump',label,time_now)) 

        #stream = StringIO.StringIO()
        #stats = pstats.Stats(p, stream=stream)
        #opt_stats = stats.print_stats('opt')
        
        #if 'api' in str(args[0]):
        #    tach_file = "nova_api"
        #else:
        #    tach_file = "compute" 
        #filename = "/home/prathyusha/TSG/"+tach_file+".txt"
        #target = open (filename, 'a')
        #target.write("%s" % (stream.getvalue()))

        #target.write("\n")

        #stats = p.getstats()
        #filtered = [(entry.totaltime, entry.callcount,
        #                 self._label(entry.code)) for entry in stats]
        #filtered = [(total, callcount, label) for total, callcount, label in
        #             filtered if label]
        #filtered.sort()
        #filtered.reverse()
        #__state['metrics'] = filtered
        return result


class Time(Collector):
    def start(self, label):
        return (label, time.time())

    def stop(self, state):
        label, start_time = state
        elapsed = time.time() - start_time
        return [(label, elapsed),]
