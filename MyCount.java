package MyCode;

import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.population.*;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.population.io.PopulationReader;
import org.matsim.core.scenario.ScenarioUtils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MyCount {

    public static void main(String[] args) {
        Scenario s = ScenarioUtils.createScenario(ConfigUtils.createConfig());
        (new PopulationReader(s)).readFile("G:/629/paris_10pct/paris_10pct/paris_population.xml");
        System.out.println("Persons size :"+(long)s.getPopulation().getPersons().size());


        Map<Long, Long> map = new HashMap<Long, Long>();

        s.getPopulation().getPersons().forEach((k,v) -> {
            Person person = v;
            if (person != null ){
                Plan plan = (Plan)person.getSelectedPlan();
                List<PlanElement> planElements = plan.getPlanElements();
                //System.out.println((long)planElements.size());

                for (PlanElement planElement : planElements) {
                    if (planElement instanceof Leg) {
                        String links = ((Leg) planElement).getRoute().getRouteDescription();

                        for (String route : links.split(" ")) {
                            if (!route.isEmpty()) {
                                try {
                                    Long r = Long.parseLong(route);
                                    if (map.containsKey(r)) {
                                        map.put(r, map.get(r) + 1);
                                    } else {
                                        map.put(r, 1L);
                                    }
                                } catch (NumberFormatException nfe) {

                                }

                            }


                        }

                    }
                }
            }
        });




        map.forEach((k,v) -> {
            System.out.println("route_id: " + k + ", count: " + v);
        });


    }
}
