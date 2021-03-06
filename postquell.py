import csdc
import json
import datetime
import orm

CRAWLDATE = "%Y%m%d%H%M%SS"

def crawldate(dt):
    return dt.strftime("%Y{:02d}%d%H%M%SS".format(dt.month - 1))

def gameline(g):
    return { 
        "name" : g.player.name,
        "start" : crawldate(g.start)
    }

def playerline(r, wk):
    if r.Game:
        return gameline(r.Game)
    else:
        return {
            "name" : r.Player.name,
            "char" : wk.char,
        }


def dumps(f, wk):
    if wk is None:
        json.dump({ "v" : { "$in" : [ "0.22.0", "0.22.1"  ] }, "$or" : [] }, f)
        return

    with orm.get_session() as s:
        return json.dump({ "v" : { "$in" : [ "0.22.0", "0.22.1" ] },
           "$not" : {
              "$or" : [
                { "$not" : { "$or" : [ { "$not" : { "type" : { "$in" : [ "zig", "br.exit", "uniq" ] }}},
                    { "type" : "zig", "lvl" : { "$in" : [ "7", "14", "21", "27"] } } ] }  },
                { "$not" : { "$or" : [ playerline(r, wk) for r in wk.sortedscorecard().with_session(s).all() ] } }
              ]
          }}, f)
