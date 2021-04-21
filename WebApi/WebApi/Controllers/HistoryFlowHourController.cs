using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Cors;

namespace WebApi.Controllers
{
    public class HistoryFlowHourController : ApiController
    {
        [HttpGet]
        [EnableCors(origins: "*", headers: "*", methods: "*")]
        public IHttpActionResult Get(String date,String staName)
        {
            String connetStr = "server=127.0.0.1;port=3306;user=root;password=root; database=zhikexing;";
            MySqlConnection conn = new MySqlConnection(connetStr);
            try
            {
                conn.Open();//建立连接
                string sql = "SELECT cnthourflow_in.c_date_in, cnthourflow_in.c_hour_in, cnthourflow_in.c_pflow_in, cnthourflow_out.c_pflow_out FROM cnthourflow_in LEFT OUTER JOIN cnthourflow_out ON(cnthourflow_in.c_date_in = cnthourflow_out.c_date_out AND cnthourflow_in.c_hour_in = cnthourflow_out.c_hour_out AND cnthourflow_in.c_sta_in = cnthourflow_out.c_sta_out) WHERE cnthourflow_in.c_sta_in = '"+ staName + "' AND cnthourflow_in.c_date_in = '"+ date + "' AND cnthourflow_in.c_hour_in >= 6 AND cnthourflow_in.c_hour_in <= 23 ORDER BY cnthourflow_in.c_date_in";
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                MySqlDataReader reader = cmd.ExecuteReader();//执行ExecuteReader()返回一个MySqlDataReader对象
                List<Object> HourFlowList = new List<object>();
                if (reader.HasRows)//如果有数据
                {
                    while (reader.Read())//初始索引是-1，执行读取下一行数据，返回值是bool
                    {
                        HourFlowList.Add(new
                        {
                            date = reader["c_date_in"],
                            hour = reader["c_hour_in"],
                            flow_in = reader["c_pflow_in"],
                            flow_out = reader["c_pflow_out"],
                        });
                    }
                }
                return Json(HourFlowList);
            }
            catch (MySqlException ex)
            {
                return Json(ex.Message);
            }
            finally
            {
                conn.Close();
            }
        }
    }
}
