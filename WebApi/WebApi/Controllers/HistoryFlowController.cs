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
    public class HistoryFlowController : ApiController
    {
        [HttpGet]
        [EnableCors(origins: "*", headers: "*", methods: "*")]
        public IHttpActionResult Get(String startDate,String endDate ,String staName)
        {
            String connetStr = "server=127.0.0.1;port=3306;user=root;password=root; database=zhikexing;";
            MySqlConnection conn = new MySqlConnection(connetStr);
            try
            {
                conn.Open();//建立连接
                string sql = "SELECT pflow_in.p_date, pflow_in.p_flow_in, pflow_out.p_flow_out FROM pflow_in LEFT OUTER JOIN pflow_out ON(pflow_in.p_date = pflow_out.p_date AND pflow_in.p_sta_name = pflow_out.p_sta_name) WHERE pflow_in.p_sta_name = '"+staName+ "' AND pflow_in.p_date >= '"+ startDate + "' AND pflow_in.p_date <= '"+ endDate + "'ORDER BY pflow_in.p_date";
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                MySqlDataReader reader = cmd.ExecuteReader();//执行ExecuteReader()返回一个MySqlDataReader对象
                List<Object> historyFlowList = new List<object>();
                if (reader.HasRows)//如果有数据
                {
                    while (reader.Read())//初始索引是-1，执行读取下一行数据，返回值是bool
                    {
                        historyFlowList.Add(new
                        {
                            date = reader["p_date"],
                            flow_in = (int)reader["p_flow_in"],
                            flow_out = (int)reader["p_flow_out"],
                        });
                    }
                }
                return Json(historyFlowList);
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
