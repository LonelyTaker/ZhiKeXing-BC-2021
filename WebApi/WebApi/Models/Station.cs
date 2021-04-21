using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApi.Models
{
    public class Station
    {
        public Station()
        {
            item = new List<Line>();
        }
        public int status = 0;
        public List<Line> item;
    }
    public class Line
    {
        public Line()
        {
            sta = new List<Sta>();
        }
        public String line_name;
        public List<Sta> sta;
    }
    public class Sta
    {
        public String sta_name;
        public int sequence;
    }
}